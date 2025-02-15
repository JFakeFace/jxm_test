#==============================================================================
# brg_scratchpad.py
#==============================================================================
# Python configuration file for BRG scratchpad system
#
# Authors: Tuan Ta
#          Philip Bedoukian
# Date  : 19/07/09

import optparse
import sys
import os
import math
import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal, warn
import argparse
import os
import sys

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.params import NULL
from m5.util import (
    addToPath,
    fatal,
    warn,
)

from gem5.isas import ISA

addToPath("../../")

from common import (
    CacheConfig,
    CpuConfig,
    MemConfig,
    ObjectList,
    Options,
    Simulation,
    ownL3
)
from common.Caches import *
from common.cpu2000 import *
from common.FileSystemConfig import config_filesystem
from ruby import Ruby
addToPath("../../")

if "--ruby" in sys.argv:
    print("Ruby----")
    Ruby.define_options(parser)
    print("Ruby")
from topologies.Crossbar import *
from network.Network import *

from common import Options
from common import Simulation
from common import CacheConfig
from common import CpuConfig
from common import MemConfig
from common.Caches import *

from math import log

#------------------------------------------------------------------------------
# Get workload process
#------------------------------------------------------------------------------

def get_processes(options):
    multiprocesses = []
    inputs = []
    outputs = []
    errouts = []
    pargs = []
    chip_ids = args.chip_id.split(";")
    workloads = options.cmd.split(';')
    if options.input != "":
        inputs = options.input.split(';')
    if options.output != "":
        outputs = options.output.split(';')
    if options.errout != "":
        errouts = options.errout.split(';')
    if options.options != "":
        pargs = options.options.split(';')

    idx = 0
    for wrkld in workloads:
        process = Process(pid = 100 + idx)
        process.executable = wrkld
        process.cwd = os.getcwd()

        if options.env:
            with open(options.env, 'r') as f:
                process.env = [line.rstrip() for line in f]

        if len(pargs) > idx:
            process.cmd = [wrkld] + pargs[idx].split()
        else:
            process.cmd = [wrkld,chip_ids[i],args.chip_num,args.N]

        if len(inputs) > idx:
            process.input = inputs[idx]
        if len(outputs) > idx:
            process.output = outputs[idx]
        if len(errouts) > idx:
            process.errout = errouts[idx]

        multiprocesses.append(process)
        idx += 1

    return multiprocesses

#------------------------------------------------------------------------------
# Make network
#------------------------------------------------------------------------------
# This creates a mesh network n_rows x n_cols
# The first (n_rows - 1) rows are connected to either CPUs and/or xcels
# The last row is connected to L2 banks

def makeMeshTopology(n_rows, n_cols, n_cpus, n_xcels, system, network, double_l2,
                     IntLink, ExtLink, Router):
  if (double_l2):
    assert(n_rows >= 3)
  else:
    assert(n_rows >= 2)
  assert(n_cols >= 1)

  num_routers = n_rows * n_cols;

  link_latency = 1
  router_latency = 1

  # all controllers
  icaches   = system.icaches
  cpu_sps   = system.scratchpads[:n_cpus]
  xcel_sps  = system.scratchpads[n_cpus:]
  l2s       = system.l2_cntrls

  print('cpu {} router {} pad {} l2s {}'.format(
    n_cpus, num_routers, len(cpu_sps), len(l2s)))
  assert(len(icaches) == n_cpus)
  assert(len(cpu_sps) == n_cpus)
  assert(n_cpus <= num_routers)
  assert(n_xcels <= num_routers)

  if (double_l2):
    assert(len(l2s) <= n_cols*2)
  else:
    assert(len(l2s) <= n_cols)

  # create all routers
  routers = [ Router(router_id = i,
                     latency = router_latency) for i in range(num_routers) ]
  network.routers = routers

  # link count used to set unique link IDs
  link_count = 0

  #--------------------------
  # Set up all external links
  #--------------------------

  ext_links = []

  router_idx = 0
  l2_idx = 0

  # l2s to first row of l2s if duplicationg
  if (double_l2):
    for i in xrange(len(l2s)/2):
      if l2_idx < len(l2s)/2:
        l2_ext_link = ExtLink(link_id   = link_count,
                              ext_node  = l2s[l2_idx],
                              int_node  = routers[i],
                              latency   = link_latency)
        l2_idx += 1
        link_count += 1
        router_idx += 1
        ext_links.append(l2_ext_link)

  # add all CPU I-caches and SPs to the first few routers
  for i in xrange(n_cpus):
    icache_ext_link = ExtLink(link_id   = link_count,
                              ext_node  = icaches[i],
                              int_node  = routers[i + router_idx],
                              latency   = link_latency)
    link_count += 1
    ext_links.append(icache_ext_link)

    cpu_sp_ext_link = ExtLink(link_id   = link_count,
                              ext_node  = cpu_sps[i],
                              int_node  = routers[i + router_idx],
                              latency   = link_latency)
    link_count += 1
    ext_links.append(cpu_sp_ext_link)

  # add all Xcel SPs to all routers
  for i in xrange(n_xcels):
    xcel_ext_link = ExtLink(link_id   = link_count,
                            ext_node  = xcel_sps[i],
                            int_node  = routers[i + router_idx],
                            latency   = link_latency)
    link_count += 1
    ext_links.append(xcel_ext_link)

  # add all l2s to bottom routers
  for i in xrange(n_cols * (n_rows - 1), num_routers):
    if l2_idx < len(l2s):
      l2_ext_link = ExtLink(link_id   = link_count,
                            ext_node  = l2s[l2_idx],
                            int_node  = routers[i],
                            latency   = link_latency)
      l2_idx += 1
      link_count += 1
      ext_links.append(l2_ext_link)

  network.ext_links = ext_links

  #--------------------------
  # Set up all internal links
  #--------------------------

  int_links = []

  # will try to take minimum weight path
  horiz_weight = 1
  verti_weight = 2


  # add another row of routers at bottom to connect

  # East output to West input links (weight = 1)
  for row in xrange(n_rows):
    for col in xrange(n_cols):
      if (col + 1 < n_cols):
        east_out  = col + (row * n_cols)
        west_in   = (col + 1) + (row * n_cols)
        int_links.append(IntLink(link_id      = link_count,
                                 src_node     = routers[east_out],
                                 dst_node     = routers[west_in],
                                 src_outport  = "East",
                                 dst_inport   = "West",
                                 latency      = link_latency,
                                 weight       = horiz_weight ))
        link_count += 1

  # West output to East input links (weight = 1)
  for row in xrange(n_rows):
    for col in xrange(n_cols):
      if (col + 1 < n_cols):
        east_in  = col + (row * n_cols)
        west_out = (col + 1) + (row * n_cols)
        int_links.append(IntLink(link_id      = link_count,
                                 src_node     = routers[west_out],
                                 dst_node     = routers[east_in],
                                 src_outport  = "West",
                                 dst_inport   = "East",
                                 latency      = link_latency,
                                 weight       = horiz_weight ))
        link_count += 1

  # North output to South input links (weight = 2)
  for col in xrange(n_cols):
    for row in xrange(n_rows):
      if (row + 1 < n_rows):
        north_out = col + (row * n_cols)
        south_in = col + ((row + 1) * n_cols)
        int_links.append(IntLink(link_id      = link_count,
                                 src_node     = routers[north_out],
                                 dst_node     = routers[south_in],
                                 src_outport  = "North",
                                 dst_inport   = "South",
                                 latency      = link_latency,
                                 weight       = verti_weight ))
        link_count += 1

  # South output to North input links (weight = 2)
  for col in xrange(n_cols):
    for row in xrange(n_rows):
      if (row + 1 < n_rows):
        north_in  = col + (row * n_cols)
        south_out = col + ((row + 1) * n_cols)
        int_links.append(IntLink(link_id      = link_count,
                                 src_node     = routers[south_out],
                                 dst_node     = routers[north_in],
                                 src_outport  = "South",
                                 dst_inport   = "North",
                                 latency      = link_latency,
                                 weight       = verti_weight ))
        link_count += 1

  network.int_links = int_links

def makeSystolicTopology(system, tiles_x, tiles_y):

  # edges harnesses to take bad packets
  system.harness = [Harness() for i in range(2 * tiles_x + 2 * tiles_y)]
  harness_idx = 0

  # get reference to the cpus already in the system
  cpus = system.cpu

  for y in range(tiles_y):
    for x in range(tiles_x):
      # do all mesh connections
      # it's important that these are done a particular order
      # so that vector idx are consistent
      # edges need to be connected to something! will do harness for now!
      idx   = x     + y         * tiles_x
      idx_r = x + 1 + y         * tiles_x
      idx_l = x - 1 + y         * tiles_x
      idx_u = x     + ( y - 1 ) * tiles_x
      idx_d = x     + ( y + 1 ) * tiles_x
    
      to_right = 0
      from_left = 2
    
      to_below = 1
      from_above = 3
    
      to_left = 2
      from_right = 0
    
      to_above = 3
      from_below = 1
    
    
      # connect to the right!
      if (x + 1 < tiles_x):
        cpus[idx].to_mesh_port[to_right] = cpus[idx_r].from_mesh_port[from_left]
      else:
        cpus[idx].to_mesh_port[to_right] = system.harness[harness_idx].from_cpu
        cpus[idx].from_mesh_port[from_right] = system.harness[harness_idx].to_cpu
        harness_idx += 1
      
      # connect to below
      if (y + 1 < tiles_y):
        cpus[idx].to_mesh_port[to_below] = cpus[idx_d].from_mesh_port[from_above]
      else:
        cpus[idx].to_mesh_port[to_below] = system.harness[harness_idx].from_cpu
        cpus[idx].from_mesh_port[from_below] = system.harness[harness_idx].to_cpu
        harness_idx += 1
      
      # connect to the left 
      if (x - 1 >= 0):
        cpus[idx].to_mesh_port[to_left] = cpus[idx_l].from_mesh_port[from_right]
      else:
        cpus[idx].to_mesh_port[to_left] = system.harness[harness_idx].from_cpu
        cpus[idx].from_mesh_port[from_left] = system.harness[harness_idx].to_cpu
        harness_idx += 1
      
      # connect to above
      if (y - 1 >= 0):
        cpus[idx].to_mesh_port[to_above] = cpus[idx_u].from_mesh_port[from_below]
      else:
        cpus[idx].to_mesh_port[to_above] = system.harness[harness_idx].from_cpu
        cpus[idx].from_mesh_port[from_above] = system.harness[harness_idx].to_cpu
        harness_idx += 1


#------------------------------------------------------------------------------
# Parse options
#------------------------------------------------------------------------------

parser = optparse.OptionParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)
Ruby.define_options(parser)

# Scratchpad size
parser.add_option("--spm-size", action="store", type="string", 
  default="4kB", help="Specify the scratchpad memory size")

# number of pending requests allowed by scratchpad
parser.add_option("--stream-width", type = "int", default = 8)

# whether to use vector stage or not
parser.add_option("--vector", action="store_true", default=False,
  help="Use vector stage in pipe")

parser.add_option("--net-width", default=4,
  help="How many words wide the network is")

parser.add_option("--hw-vlen", default=4,
  help="Hardware vector length in number of words")

parser.add_option("--mesh-queue-len", default=2,
  help="How many instructions can be stored between cores in vector mode")

parser.add_option("--llc-max-size", default="16kB",
  help="How large should llc slices be if more than 8slices")

parser.add_option("--dram-bw", default=16,
  help="Target dram bandwidth in gb/s")

(options, args) = parser.parse_args()

# set large mem-size needed for larger problem sizes
options.mem_size = '1GB'

# figure out system size
n_cpus  = options.num_cpus
n_xcels = 0 #options.num_xcels
n_tiles = n_cpus + n_xcels

double_L2 = True

# mesh size is determined by the number of xcels and device cpus
n_cols  = int(math.sqrt(n_tiles))

# this extra row of routers is for the l2s
n_rows  = n_cols + 1

n_l2s   = n_cols

# add another row if doing 2nd row on edge
if (double_L2):
  n_rows += 1

if (double_L2):
  n_l2s += n_cols


# network classes
#assert(options.network == "garnet2.0")
options.network = "garnet2.0"
# virt_channels = 64
# options.vcs_per_vnet = virt_channels
NetworkClass = GarnetNetwork
IntLinkClass = GarnetIntLink
ExtLinkClass = GarnetExtLink
RouterClass = GarnetRouter
InterfaceClass = GarnetNetworkInterface

# Do not support multi-process simulation
process = get_processes(options)[0]

#------------------------------------------------------------------------------
# Construct CPUs
#------------------------------------------------------------------------------

if (options.cpu_type == 'DerivO3CPU'):
  CPUClass = CpuConfig.get('DerivO3CPU')

  # 4-way, 16lq+16sq (default 8-way, 32lq+32sq)
  cpuWidth = 4
  CPUClass.fetchWidth = cpuWidth
  CPUClass.decodeWidth = cpuWidth
  CPUClass.renameWidth = cpuWidth
  CPUClass.dispatchWidth = cpuWidth
  CPUClass.issueWidth = cpuWidth
  CPUClass.wbWidth = cpuWidth
  CPUClass.commitWidth = cpuWidth
  CPUClass.squashWidth = cpuWidth

  CPUClass.LQEntries = 16
  CPUClass.SQEntries = 16

  # make sure stream width matches lsq size
  options.stream_width = CPUClass.LQEntries + CPUClass.SQEntries
else:
  if (options.cpu_type != 'IOCPU'):
    print('WARNING: Only support IOCPU (w or w/o vector) or DerivO3Cpu (w/o vector)')
  # CPU class
  CPUClass = IOCPU (
    includeVector = options.vector,
    meshBufferSize = options.mesh_queue_len,
    numROBEntries = 8,
    # remember to set in util.h
    hw_vector_length = options.hw_vlen
    # latencies from https://github.com/bespoke-silicon-group/riscv-gcc/blob/bsg_manycore_gcc/gcc/config/riscv/bsg_vanilla_2020.md
    ,
    intAluOpLatency = 1,
    intMulOpLatency = 2,
    divOpLatency    = 20,
    fpAluOpLatency  = 3,
    fpMulOpLatency  = 3
    # , numLoadQueueEntries = 8,
    # numStoreQueueEntries = 8
  )

# Create top-level system
system = System(cpu = [ CPUClass(cpu_id = i) for i in xrange(n_cpus) ],
                        mem_mode = CPUClass.memory_mode(),
                        mem_ranges = [ AddrRange(options.mem_size) ],
                        cache_line_size = options.cacheline_size)

# Create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage = options.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(clock =  options.sys_clock,
                                   voltage_domain = system.voltage_domain)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(clock = options.sys_clock,
                                       voltage_domain =
                                       system.cpu_voltage_domain)

# All cpus belong to a common cpu_clk_domain, therefore running at a common
# frequency.
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain

# Assign workload to CPUs
for i in xrange(n_cpus):
  system.cpu[i].workload = process
  system.cpu[i].workload[0].release = '99.99.99'
  system.cpu[i].createThreads()

#------------------------------------------------------------------------------
# Construct Ruby memory system
#------------------------------------------------------------------------------

system.ruby = RubySystem(block_size_bytes=options.cacheline_size)

# Construct network
network = NetworkClass (ruby_system = system.ruby,
                        routers = [],
                        ext_links = [],
                        int_links = [],
                        netifs = [],
                        number_of_virtual_networks = 2, # what does it mean to have two networks??
                        # vcs_per_vnet=32
                        )
                        

# Scratchpads
#n_scratchpads = n_cpus + n_xcels
n_scratchpads = n_tiles
scratchpads = []

for i in xrange(n_scratchpads):
  sp = Scratchpad(version           = i,
                  ruby_system       = system.ruby,
                  sp_size           = AddrRange(options.spm_size).size(),
                  dram_size         = AddrRange(options.mem_size).size(),
                  num_l2s           = n_l2s,
                  grid_dim_x        = n_cols,
                  grid_dim_y        = n_cols,
                  # might be too big but can solve by having spad not remember
                  # store noacks like it does for prefetch
                  maxNumPendingReqs = options.stream_width,
                  prefetchBufSize   = 0, # don't allow to go over
                  numFrameCntrs     = 5,
                  cpu               = system.cpu[i])

  sp.memReqBuffer             = MessageBuffer(ordered = True)
  sp.memReqBuffer.master      = network.slave

  sp.memRespBuffer            = MessageBuffer(ordered = True)
  sp.memRespBuffer.slave      = network.master

  sp.remoteReqBuffer          = MessageBuffer(ordered = True)
  sp.remoteReqBuffer.slave    = network.master

  sp.remoteRespBuffer         = MessageBuffer(ordered = True)
  sp.remoteRespBuffer.master  = network.slave

  scratchpads.append(sp)

system.scratchpads = scratchpads

# L1-I caches and sequencers
n_icaches = n_cpus
icache_cntrls = []
sequencers = []
for i in xrange(n_icaches):
  icache = RubyCache(size = '4kB', assoc = 2)
  icache_cntrl = L1Cache_Controller(version = i,
                                    L1cache = icache,
                                    transitions_per_cycle = options.ports,
                                    ruby_system = system.ruby)

  icache_cntrl.requestToNetwork          = MessageBuffer(ordered = True)
  icache_cntrl.requestToNetwork.master   = network.slave
  icache_cntrl.responseFromNetwork       = MessageBuffer(ordered = True)
  icache_cntrl.responseFromNetwork.slave = network.master
  icache_cntrl.mandatoryQueue            = MessageBuffer(ordered = True)

  sequencer = RubySequencer()
  sequencer.version = i
  sequencer.icache = icache
  # only 1 cycle resp latency now (so 1 total)
  # need to hack sequencer to turn 1 cycle into a 1 tick wait 
  # (effectively 0 cycles but plays nicely with wakeup queues)
  sequencer.icache_hit_latency = 0
  sequencer.dcache = icache
  sequencer.ruby_system = system.ruby
  sequencer.is_cpu_sequencer = True

  icache_cntrl.sequencer = sequencer

  icache_cntrls.append(icache_cntrl)
  sequencers.append(sequencer)

system.icaches = icache_cntrls
system.ruby.num_of_sequencers = len(sequencers)
system.ruby.number_of_virtual_networks = 2

# L2 cache
l2_cntrls = []

if n_l2s == 1:
  l2_size = '256kB'
elif n_l2s == 2:
  l2_size = '128kB'
elif n_l2s == 4:
  l2_size = '64kB'
elif n_l2s == 8:
  l2_size = '32kB'
elif n_l2s == 16:
  l2_size = options.llc_max_size
elif n_l2s % n_cols == 0:
  l2_size = options.llc_max_size
else:
  fatal("Invalid number of L2 banks")

for i in xrange(n_l2s):
  l2_cache = RubyCache(size = l2_size, assoc = 4)
  l2_cntrl = L2Cache_Controller(version = i,
                                cacheMemory = l2_cache,
                                transitions_per_cycle = 16,
                                meshDimX = n_cols,
                                meshDimY = n_cols,
                                ruby_system = system.ruby
                                ,
                                netWidth = options.net_width,
                                cache_resp_latency = 1,
                                to_memory_controller_latency = 1,
                                mem_to_cpu_latency = 1 # TODO this needs to be the same as cache_resp_latency b/c same ordered queue?
                                , number_of_TBEs = 64
                                )
                                #number_of_TBEs = 1)

  l2_cntrl.requestToLLC           = MessageBuffer(ordered = True)
  l2_cntrl.requestToLLC.slave     = network.master

  l2_cntrl.responseFromLLC        = MessageBuffer(ordered = True)
  l2_cntrl.responseFromLLC.master = network.slave

  l2_cntrl.responseFromMemory     = MessageBuffer(ordered = True)

  l2_cntrls.append(l2_cntrl)


system.l2_cntrls = l2_cntrls

#------------------------------------------------------------------------------
# Connect all controllers to network
#------------------------------------------------------------------------------

makeMeshTopology(n_rows, n_cols, n_cpus, n_xcels, system, network, double_L2, 
                 IntLinkClass, ExtLinkClass, RouterClass)

init_network(options, network, InterfaceClass)

system.network = network

system.ruby.sys_port_proxy = RubyPortProxy(ruby_system = system.ruby)
system.system_port = system.ruby.sys_port_proxy.slave

#------------------------------------------------------------------------------
# Construct systolic network
#------------------------------------------------------------------------------

if (options.vector and options.cpu_type == 'IOCPU'):
  eff_rows = n_rows - 1
  if (double_L2):
    eff_rows = n_rows - 2
  makeSystolicTopology(system, eff_rows, n_cols)

#------------------------------------------------------------------------------
# Construct memory controller
#------------------------------------------------------------------------------

system.mem_mode = 'timing'
system.mem_ranges = [ AddrRange(options.mem_size) ]


# so HammerBlade uses 1 channels per 16 caches (which is 16GB/s total)

# HBM_1000_4H_1x128 * 8  (HBMv1)
# eac is 16GB/s so -> 8B/c (@1GHZ). so 16*num_channel = 128B/c
# HBM_1000_4H_1x64  * 16 (HBMv2)
# each is 8GB/s, -> 8B/c (@1GHZ). so 8*num_channel B/c
bytes_per_cycle = options.dram_bw

system.mem_ctrl = SimpleMemory()
system.mem_ctrl.latency = '60ns' 
system.mem_ctrl.bandwidth = str(bytes_per_cycle) + 'GB/s' # HBM is 128GB/s HBM2 is 256GB/s (1024bit bus...high overhead to route, slower clock than ddr but comparable?)
system.mem_ctrl.range = system.mem_ranges[0]

# num_channels = 2
# nbr_mem_ctrls = num_channels
# intlv_size = max(128, system.cache_line_size.value)
# intlv_bits = int(math.log(nbr_mem_ctrls, 2))
# mem_ctrls = []
# for i in range(num_channels):
#   mc = MemConfig.create_mem_ctrl(HBM_1000_4H_1x128, system.mem_ranges[0], i, nbr_mem_ctrls, intlv_bits, intlv_size)
#   mem_ctrls.append(mc)
# system.mem_ctrls = mem_ctrls

#------------------------------------------------------------------------------
# Construct a crossbar that connects L2s and mem_ctrl
#------------------------------------------------------------------------------
# TODO is this crossbar realistic w/ multiple channels? or should one channel be connected to one cache? (if so should do HBMv2 w/ 16 channels b/c nicer link)
system.l2_bus = NoncoherentXBar()

# 16 bytes per cycle. This is set to match with the mem_ctrl.bandwidth
system.l2_bus.width = bytes_per_cycle
system.l2_bus.frontend_latency = 1
system.l2_bus.forward_latency = 1
system.l2_bus.response_latency = 1
system.l2_bus.clk_domain = system.clk_domain

for i in xrange(n_l2s):
  system.l2_bus.slave = system.l2_cntrls[i].memory

# for i in xrange(nbr_mem_ctrls):
#   system.l2_bus.master = system.mem_ctrls[i].port

system.l2_bus.master = system.mem_ctrl.port

#------------------------------------------------------------------------------
# Connect memory controller and CPUs to the Ruby system
#------------------------------------------------------------------------------

#system.mem_ctrl.port = l2_cntrl.memory

for i in xrange(n_cpus):
  system.cpu[i].createInterruptController()
  system.cpu[i].icache_port = sequencers[i].slave
  system.cpu[i].dcache_port = system.scratchpads[i].cpu_port

for i in xrange(n_xcels):
  system.xcel[i].mem_port = system.scratchpads[n_cpus + i].cpu_port

#------------------------------------------------------------------------------
# Simulation
#------------------------------------------------------------------------------

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)

# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
print('Exit code %i' % exit_event.getCode())

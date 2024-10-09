##################################
# Example Script for Running BFS benchmark
# for 10K instructions on 16c CHIPS system
#
# Written By: Tushar Krishna (tushar@ece.gatech.edu)
# Last Updated: Feb 5, 2019
##################################

## How to run
#./my_scripts/run_demo.sh "<additional_options>"

# Examples to try:
#./my_scripts/run_demo.sh "--interposer-link-width=32"
#./my_scripts/run_demo.sh "--interposer-link-width=8"
#./my_scripts/run_demo.sh "--interposer-link-width=32 --clip-logic-ifc-delay=12"



cpu_type=TimingSimpleCPU

# Cache Parameters
# L1
l1_size='16kB'
l1_assoc=4

# Total L2 = 2MB
# L2 per tile:
l2_size='128kB'
l2_assoc=8


./build/X86/gem5.opt \
-d my_outdir \
configs/example/garnet_synth_traffic.py \
--num-cpus=3 \
--l1d_size=${l1_size} --l1i_size=${l1_size} --l1d_assoc=${l1_assoc} \
--num-l2caches=3 \
--l2_size=${l2_size} --l2_assoc=${l2_assoc} \
--num-dirs=4 \
--ruby --mem-size=4096MB \
--topology="CHIPS_Multicore_MemCtrlChiplet4" \
--mesh-rows=1 \
#--debug-flags=GarnetSyntheticTraffic \
--network=garnet \
--sim-cycles=1000000 \
--inj-vnet=0 \
--synthetic=uniform_random \
--injectionrate=1 \
--single-sender-id=0

$1


# Print Stats
echo
echo "CHIPS Demo: Stats:"
grep "sim_ticks" my_outdir/stats.txt
grep "average_packet_latency" my_outdir/stats.txt

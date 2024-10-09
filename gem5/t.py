import m5
from m5.objects import *
from m5.util import convert

# 创建一个系统，它是仿真的根对象
system = System()

# 设置时钟频率和电压
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# 设置内存模式，以及内存大小
system.mem_mode = 'timing'  # 选择timing模式来模拟内存时序
system.mem_ranges = [AddrRange('512MB')]

# 创建一个简单的内存总线
system.membus = SystemXBar()

# 创建一个CPU
system.cpu = TimingSimpleCPU()

# 创建一个内存控制器
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.mem_side = system.membus.mem_side_ports

# 设置系统端口
system.system_port = system.membus.cpu_side_ports

# 设置CPU的时钟域
system.cpu.clk_domain = system.clk_domain

# 创建一个自定义事件，用于发送数据包
class SendPacketEvent(Event):
    def __init__(self, cpu):
        super(SendPacketEvent, self).__init__()
        self.cpu = cpu

    def process(self):
        # 创建并发送一个数据包
        addr = 0x1000  # 目标地址
        size = 64  # 数据大小
        req = Request(dest=addr, size=size, flags=Request.WRITE,
                      sender=self.cpu.instRequestorId())
        pkt = Packet(req, Packet.WRITE, data="Hello from CPU!")
        pkt.data_uint64 = 0x1  # 可以发送任何数据，这里发送一个简单的整数
        self.cpu.dcachePort.sendTimingReq(pkt)  # 发送数据包
        print("Packet sent by CPU")

# 创建和连接CPU的端口
system.cpu.createInterruptController()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

# 设置工作负载
system.cpu.workload = SEWorkload.init_compatible("tests/test-progs/hello/bin/x86/linux/hello")

# 设置系统开始运行的入口点
system.cpu.createThreads()

# 设置仿真器的运行配置
root = Root(full_system=False, system=system)
m5.instantiate()

# 安排发送数据包的事件
event = SendPacketEvent(system.cpu)
m5.schedule(event, m5.curTick() + 100)

# 运行仿真
print("开始仿真...")
exit_event = m5.simulate()
print('仿真结束退出代码: %s' % exit_event.getCause())


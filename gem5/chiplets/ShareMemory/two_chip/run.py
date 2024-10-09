import subprocess

commands = [
    "../../../build/X86/gem5.opt -d out1 ../../../configs/deprecated/example/se.py --cmd=./c0 --cpu-type=DerivO3CPU --caches --mem-size=1GB --num-cpus 1 --chip_id 0",
    "../../../build/X86/gem5.opt -d out2 ../../../configs/deprecated/example/se.py --cmd=./c1 --cpu-type=DerivO3CPU --caches --mem-size=1GB --num-cpus 1 --chip_id 1"
]

for command in commands:
    process = subprocess.Popen(command, shell=True)
    process.wait()


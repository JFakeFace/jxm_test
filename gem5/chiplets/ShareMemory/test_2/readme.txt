g++ -o a1 a1.cpp -lrt -lpthread
../../build/X86/gem5.opt ../../configs/deprecated/example/se.py --cmd="./a;./b" --cpu-type=DerivO3CPU --caches --mem-size=1GB --num-cpus 2


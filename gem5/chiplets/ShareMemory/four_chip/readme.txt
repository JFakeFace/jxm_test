../../../build/X86/gem5.opt ../../../configs/deprecated/example/se.py --cmd="./c0;./c1" --cpu-type=DerivO3CPU --caches --mem-size=1GB --num-cpus 2 --chip_id '0;1' --chip_num 2 --N 4  



settask -c 0 mpiexec -n 1 ./mpi_sender 0 2 4 : -c 1 -n 1 ./mpi_receiver 1 2 4

1410878000 1 3354738000 30619566000 
1491784000 2 3261498000 22371490500


4699607000
1324632500

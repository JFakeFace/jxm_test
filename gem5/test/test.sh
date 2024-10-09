#!/bin/bash

# 定义总的CPU核心数和矩阵大小
CHIP_NUM=2  
MATRIX_SIZE=4  

# 循环启动每个CPU的进程，并将每个进程绑定到一个核心
for (( i=0; i<${CHIP_NUM}; i++ ))
do
    taskset -c $i ./c $i $CHIP_NUM $MATRIX_SIZE &
done


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
 
using namespace std;
#include "m5ops.h"
/*
本示例示范 2 个 chiplet 做 10*10 的矩阵乘工作，假设结果为 C，则 C 的大小为
10*10，用一维矩阵储存，则 chiplet0 计算矩阵乘 C 索引从 0 到 500*249 的结果，而
chiplet1 计算剩下的结果。
*/
extern "C" 
{
	int main() {
        m5_gadia_call(0,1,2,3);
	return 0;
	}
}

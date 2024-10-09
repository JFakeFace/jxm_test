#include <iostream>
#include <vector>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <semaphore.h>
#include <cstdlib>

int main() {
    const int N = 4;
    const int SIZE = N * N * sizeof(int);
    const char* names[3] = {"/shm_A", "/shm_B", "/shm_C"};
    int shm_fds[3];
    int* ptrs[3];

    // 等待信号量准备好
    sem_t* sem = sem_open("/sem_calc", 0);
    sem_wait(sem);

    // 映射共享内存
    for (int i = 0; i < 3; i++) {
        shm_fds[i] = shm_open(names[i], O_RDWR, 0666);
        ptrs[i] = static_cast<int*>(mmap(0, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fds[i], 0));
    }

    // 执行矩阵乘法
    std::vector<int> result(N * N, 0);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                result[i * N + j] += ptrs[0][i * N + k] * ptrs[1][k * N + j];
            }
        }
    }

    // 打印结果
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            std::cout << result[i * N + j] << " ";
        }
        std::cout << std::endl;
    }

    // 释放映射内存并关闭共享内存
    for (int i = 0; i < 3; i++) {
        munmap(ptrs[i], SIZE);
        close(shm_fds[i]);
    }

    sem_close(sem);
    sem_unlink("/sem_calc");

    return 0;
}


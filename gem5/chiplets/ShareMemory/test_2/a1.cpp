#include <iostream>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <cstring>
#include <semaphore.h>

int main() {
    const int N = 4;  // 矩阵大小
    const int SIZE = N * N * sizeof(int);
    const char* names[3] = {"/shm_A", "/shm_B", "/shm_C"};
    int shm_fds[3];
    int* ptrs[3];

    // 创建和映射共享内存
    for (int i = 0; i < 3; i++) {
        shm_fds[i] = shm_open(names[i], O_CREAT | O_RDWR, 0666);
        ftruncate(shm_fds[i], SIZE);
        ptrs[i] = static_cast<int*>(mmap(0, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fds[i], 0));
        if (ptrs[i] == MAP_FAILED) {
            perror("Error mapping memory");
            close(shm_fds[i]);  // Close file descriptor if mmap fails
            return EXIT_FAILURE;
        }
    }

    // 初始化矩阵A和矩阵B
    for (int i = 0; i < N * N; i++) {
        ptrs[0][i] = 1; // Fill matrix A with 1s
        ptrs[1][i] = 2; // Fill matrix B with 2s
    }

    // 创建信号量，用于同步
    sem_t* sem = sem_open("/sem_calc", O_CREAT, 0666, 0);

    // 释放映射内存但不关闭共享内存
    for (int i = 0; i < 3; i++) {
        munmap(ptrs[i], SIZE);
    }

    // 通知计算进程开始工作
    sem_post(sem);
    sem_close(sem);

    return 0;
}


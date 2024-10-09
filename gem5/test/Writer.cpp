#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

#define SHM_NAME "/my_shm"
#define SHM_SIZE 4096

int main() {
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        return EXIT_FAILURE;
    }

    if (ftruncate(shm_fd, SHM_SIZE) == -1) {
        perror("ftruncate");
        return EXIT_FAILURE;
    }

    void *ptr = mmap(0, SHM_SIZE, PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        return EXIT_FAILURE;
    }

    char message[] = "Hello from writer!";
    sprintf((char*)ptr, "%s", message);


    printf("Data written in memory: %s\n", message);

    munmap(ptr, SHM_SIZE);
    close(shm_fd);

    return EXIT_SUCCESS;
}


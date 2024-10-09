#include <iostream>
#include <vector>
#include <cstdlib>  // for atoi
#include <cstring>  // for memset
#include <sys/mman.h>
#include <fcntl.h>  // for O_CREAT
#include <unistd.h> // for close, ftruncate, unlink
#include <fstream>  // for file operations

using namespace std;

const char* SHM_NAME = "/shm_example";
const char* LOCK_FILE = "/tmp/shm_example_lock";

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cerr << "Error: Please provide chip id, number of chips, and matrix size as command-line arguments." << endl;
        return 1;
    }

    int chip_id = atoi(argv[1]);
    int chip_num = atoi(argv[2]);
    int N = atoi(argv[3]);

    size_t shm_size = N * N * sizeof(int);
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("Error opening shared memory");
        return 1;
    }

    if (ftruncate(shm_fd, shm_size) == -1) {
        perror("Error setting size of shared memory");
        close(shm_fd);
        shm_unlink(SHM_NAME);
        return 1;
    }

    int* shm_ptr = (int*)mmap(nullptr, shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_ptr == MAP_FAILED) {
        perror("Error mapping shared memory");
        close(shm_fd);
        shm_unlink(SHM_NAME);
        return 1;
    }

    if (chip_id == 0) {
        memset(shm_ptr, 0, shm_size);
        ofstream lock_file(LOCK_FILE);
        if (!lock_file) {
            cerr << "Failed to create lock file." << endl;
            munmap(shm_ptr, shm_size);
            close(shm_fd);
            shm_unlink(SHM_NAME);
            return 1;
        }
    } else {
        while (!ifstream(LOCK_FILE)) {
            usleep(100000);  // Poll every 100 ms
        }
    }

    vector<vector<int>> v1(N, vector<int>(N, 1));
    vector<vector<int>> v2(N, vector<int>(N, 1));

    // Perform matrix multiplication directly in shared memory
    for (int i = N / chip_num * chip_id; i < N / chip_num * (chip_id + 1); i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                shm_ptr[i * N + j] += v1[i][k] * v2[k][j];
            }
        }
    }

    if (chip_id == 0) {
        // Wait for a moment to ensure all processes have completed their work
        sleep(1);  // A more robust solution would involve proper inter-process communication
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                cout << shm_ptr[i * N + j] << " ";
            }
            cout << endl;
        }
        munmap(shm_ptr, shm_size);
        close(shm_fd);
        shm_unlink(SHM_NAME);
        unlink(LOCK_FILE);
    } else {
        // Proper synchronization should be used instead of sleep
        sleep(1);  // Allow time for the output
        munmap(shm_ptr, shm_size);
        close(shm_fd);
    }

    return 0;
}


#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cerrno>
#include <cstring>  // For strerror

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cout << "Error: Please provide a chip id, number of chips, and matrix size as command-line arguments." << endl;
        return 1; // Returning 1 indicates an error
    }

    int chip_id = atoi(argv[1]);
    int chip_num = atoi(argv[2]);
    int N = atoi(argv[3]);

    if (chip_id == -1) {
        cout << "Error: Invalid chip id provided." << endl;
        return 1;
    }

    vector<vector<int>> v1(N, vector<int>(N, 1));
    vector<vector<int>> v2(N, vector<int>(N, 1));
    vector<vector<int>> v3(N, vector<int>(N, 0));

    int rows_per_chip = N / chip_num;
    int remainder = N % chip_num;
    int start = chip_id < remainder ? chip_id * (rows_per_chip + 1) : chip_id * rows_per_chip + remainder;
    int end = start + (chip_id < remainder ? rows_per_chip + 1 : rows_per_chip);

        const char* fifoPath = "communication0";



    int fd = open(fifoPath, O_WRONLY | O_NONBLOCK); // Open the fifo in non-blocking mode
    int cnt = 0;
    while (fd == -1) {
        perror("Failed to open fifo for writing");
        fd = open(fifoPath, O_WRONLY | O_NONBLOCK); // Open the fifo in non-blocking mode
	cnt += 1;
        if(cnt == 15) break;
    }

    string message;
    for (int i = start; i < end; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                v3[i][j] += v1[i][k] * v2[k][j];
            }
            message = to_string(chip_id) + " " + to_string(0) + " " + to_string(0) + " " + to_string(i) + " " + to_string(j) + " " + to_string(v3[i][j]) + "\n";
            if (write(fd, message.c_str(), message.size()) == -1) {
                if (errno == EAGAIN || errno == EWOULDBLOCK) {
                    cout << "Pipe is full, retrying..." << endl;
                    // Optional: Implement a retry mechanism
                } else {
                    cerr << "Failed to write to fifo: " << strerror(errno) << endl;
                }
            }       
        }
    }

    message = to_string(chip_id) + " " + to_string(0) + " " + to_string(0) + " " + to_string(-1) + " " + to_string(-1) + " " + to_string(-2) + "\n";
    if (write(fd, message.c_str(), message.size()) == -1) {
        cerr << "Failed to write end message to fifo: " << strerror(errno) << endl;
    }

    //close(fd);
    return 0;
}


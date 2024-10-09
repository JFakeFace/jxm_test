#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "Message.h"
#include <vector>
#include <cstdlib> // for atoi
#include <cstdlib> // for exit
#include<cmath>
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cstring>
using namespace std;
int chip_num = 4;
int N = 8;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Error: Please provide a chip id as a command-line argument." << endl;
        return 1; // Returning 1 indicates an error
    }
    int cnt = 0;
    int chip_id = atoi(argv[1]);
    chip_num = atoi(argv[2]);
    N = atoi(argv[3]);
    if (chip_id == -1) {
        cout << "Error: Invalid chip id provided." << endl;
        exit(1);
    }

    //if (mkfifo(fifoPath, 0666) == -1 && errno != EEXIST) {
    //    cerr << "Failed to create fifo." << endl;
       // return 1;
  //  }

    vector<vector<int>> v1(N, vector<int>(N, 1));
    vector<vector<int>> v2(N, vector<int>(N, 1));
    vector<vector<int>> v3(N, vector<int>(N, 0));

    int rows_per_chip = N / chip_num;
    int remainder = N % chip_num;
    int start = chip_id < remainder ? chip_id * (rows_per_chip + 1) : chip_id * rows_per_chip + remainder;
    int end = start + (chip_id < remainder ? rows_per_chip + 1 : rows_per_chip);

    for (int i = start; i < end; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                v3[i][j] += v1[i][k] * v2[k][j];
            }
        }
    }


    string line;
    // 创建命名管道，如果已存在则无操作
    const char* fifoPath = "communication";
    // 打开chiplet num 不为1的通道，并读取
    for(int i = 1;i <= chip_num;i++) {
        // 直到读取到-2结束输入
        const char* name = fifoPath + char(i + '0');
        int fd = open(name, O_RDONLY|O_NONBLOCK);
        if (fd == -1) {
            perror("Failed to open fifo for writing");
            return 1;
        }
        std::string receivedInput;
        char buffer[1024];
        int flag  = 0;
        while(true) {
            int bytesRead = read(fd, buffer, sizeof(buffer) - 1);
            if (bytesRead > 0) {
                buffer[bytesRead] = '\0';
                receivedInput.append(buffer);
                std::string line;
                size_t pos = 0;
                while ((pos = receivedInput.find('\n')) != std::string::npos) {
                    line = receivedInput.substr(0, pos);
                    stringstream ss(line);
                    Message msg;
                    ss >> msg.src_chip >> msg.dest_chip >> msg.next_chip >> msg.x >> msg.y >> msg.data;
                    cout << "Received: " << msg.src_chip << " " << msg.dest_chip << " " << msg.next_chip << " " << msg.x << " " << msg.y << " " << msg.data << endl;
                    receivedInput.erase(0, pos + 1);
                    if (msg.data == -2) {
                        flag = 1;
                        break;
                    } else {
                        v3[msg.x][msg.y] += msg.data;
                }

            }
        }
        if(flag) {
            break;
        }
        }
    }

   for (int i = 0; i < N; i++) {
       for (int j = 0; j < N; j++) {
           cout << v3[i][j] << " ";
      }
        cout << endl;
    }

    return 0;
}


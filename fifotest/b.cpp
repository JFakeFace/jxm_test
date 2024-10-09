#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cstring>
#include <sstream>

int main() {
    const char* fifoPath = "/tmp/my_fifo";

    // 创建命名管道，如果已存在则无操作
    if (mkfifo(fifoPath, 0666) == -1 && errno != EEXIST) {
        std::cerr << "Failed to create fifo." << std::endl;
        return 1;
    }

    int fd = open(fifoPath, O_RDONLY);
    if (fd == -1) {
        std::cerr << "Failed to open fifo for reading." << std::endl;
        return 1;
    }

    std::string receivedInput;
    char buffer[1024];

    while (true) {
        int bytesRead = read(fd, buffer, sizeof(buffer) - 1);
        if (bytesRead > 0) {
            buffer[bytesRead] = '\0';
            receivedInput.append(buffer);

            std::string line;
            size_t pos = 0;
            // 处理每一行直到找不到新的换行符
            while ((pos = receivedInput.find('\n')) != std::string::npos) {
                line = receivedInput.substr(0, pos);
                if (line == "END") {
                    break;
                }
                std::cout << "Received: " << line << std::endl;
                receivedInput.erase(0, pos + 1);
            }

        } else if (bytesRead == 0) {
            // 如果bytesRead为0，表示管道的另一端已经关闭
            break;
        } else {
            // 出错处理
            std::cerr << "Read error." << std::endl;
            break;
        }
    }

    close(fd);  // 关闭文件描述符
    unlink(fifoPath);  // 删除管道文件
    return 0;
}


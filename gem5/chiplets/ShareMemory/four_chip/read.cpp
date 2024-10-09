#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <cstring>
#include <errno.h>

int main() {
    const char* fifoPath = "communication0";
    int fd;

    // 尝试打开管道以进行读取
    fd = open(fifoPath, O_RDONLY | O_NONBLOCK); // 非阻塞模式
    if (fd == -1) {
        std::cerr << "Failed to open fifo for reading: " << strerror(errno) << std::endl;
        return 1;
    }

    std::cout << "Reading from the FIFO...\n";

    char ch;
    std::string line;
    while (true) {
        ssize_t count = read(fd, &ch, 1);
        if (count == -1) {
            // 如果在读取时出错
            if (errno == EAGAIN) {
                std::cout << "No data available right now, waiting..." << std::endl;
                sleep(1); // 稍等片刻后重试
                continue;
            } else {
                std::cerr << "Read error: " << strerror(errno) << std::endl;
                break;
            }
        } else if (count == 0) {
            // 如果读到文件末尾
            if (!line.empty()) {
                std::cout << line << std::endl; // 输出最后一行（如果有）
            }
            break;
        } else {
            if (ch == '\n') {
                std::cout << line << std::endl;
                line.clear();
            } else {
                line += ch;
            }
        }
    }

    close(fd); // 关闭文件描述符

    std::cout << "Finished reading from the FIFO." << std::endl;
    return 0;
}


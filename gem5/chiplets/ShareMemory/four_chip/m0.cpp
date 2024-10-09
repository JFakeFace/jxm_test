// writer.cpp
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cstring>

using namespace std;

int main() {
    const char* fifoPath = "communication0";

    // 创建FIFO
    if (mkfifo(fifoPath, 0666) == -1) {
        if (errno != EEXIST) {
            cerr << "Failed to create FIFO: " << strerror(errno) << endl;
            return 1;
        }
    }

    // 打开FIFO用于写入
    int fd = open(fifoPath, O_WRONLY);
    if (fd == -1) {
        cerr << "Failed to open FIFO for writing: " << strerror(errno) << endl;
        return 1;
    }

    // 写入数据到FIFO
    string data = "Hello from Writer!\n";
    if (write(fd, data.c_str(), data.size()) == -1) {
        cerr << "Failed to write to FIFO: " << strerror(errno) << endl;
        close(fd);
        return 1;
    }

    cout << "Message written to FIFO." << endl;
    close(fd);
    return 0;
}


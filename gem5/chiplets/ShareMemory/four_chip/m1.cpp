// reader.cpp
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cstring>

using namespace std;

int main() {
    const char* fifoPath = "communication0";

    // 打开FIFO用于读取
    int fd = open(fifoPath, O_RDONLY);
    if (fd == -1) {
        cerr << "Failed to open FIFO for reading: " << strerror(errno) << endl;
        return 1;
    }

    char buf[1024];
    ssize_t numRead = read(fd, buf, sizeof(buf) - 1);
    if (numRead == -1) {
        cerr << "Failed to read from FIFO: " << strerror(errno) << endl;
        close(fd);
        return 1;
    }

    buf[numRead] = '\0'; // 确保字符串正确终止
    cout << "Received from FIFO: " << buf << endl;
    close(fd);
    return 0;
}


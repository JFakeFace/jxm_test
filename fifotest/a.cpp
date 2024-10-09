#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cstring>

int main() {
    const char* fifoPath = "/tmp/my_fifo";


    mkfifo(fifoPath, 0666);

    const char* messages[] = {"Hello", "from", "the", "writer", "program", "END", nullptr};


    int fd = open(fifoPath, O_WRONLY);
    if (fd == -1) {
        std::cerr << "Failed to open fifo for writing." << std::endl;
        return 1;
    }

    for (int i = 0; messages[i] != nullptr; ++i) {
        write(fd, messages[i], strlen(messages[i]));
        write(fd, "\n", 1);
        sleep(1); 
    }

    close(fd);  
    return 0;
}


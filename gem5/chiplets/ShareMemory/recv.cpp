// receiver.cpp
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main() {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(12345);
    addr.sin_addr.s_addr = INADDR_ANY;

    bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
    listen(sockfd, 1);
    int clientfd = accept(sockfd, NULL, NULL);
    int number;
    recv(clientfd, &number, sizeof(number), 0);
    std::cout << "Received: " << number << std::endl;
    close(clientfd);
    close(sockfd);
    return 0;
}


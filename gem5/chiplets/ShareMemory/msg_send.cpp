#include <iostream>
#include <mqueue.h>
#include <cstring>
#include <cstdlib>

int main() {
    mqd_t mq;
    const char* queueName = "/test_queue";
    struct mq_attr attr;
    attr.mq_flags = 0; // 阻塞模式
    attr.mq_maxmsg = 10; // 队列中最大消息数
    attr.mq_msgsize = 128; // 每个消息的最大大小
    attr.mq_curmsgs = 0; // 当前队列中的消息数，初始化不用设

    // 创建或打开消息队列
    mq = mq_open(queueName, O_CREAT | O_WRONLY, 0644, &attr);
    if (mq == -1) {
        perror("Creating queue");
        return 1;
    }

    // 发送消息
    char buffer[128] = "Hello from Sender";
    if (mq_send(mq, buffer, strlen(buffer) + 1, 0) == -1) {
        perror("Sending");
        return 1;
    }

    std::cout << "Message sent: " << buffer << std::endl;

    // 关闭消息队列
    mq_close(mq);
    return 0;
}


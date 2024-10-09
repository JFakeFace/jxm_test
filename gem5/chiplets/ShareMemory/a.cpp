#include <iostream>
#include <string>
extern "C" {
#include "m5/m5ops.h"
}

int main() {
    std::string input;
    while (1) { // 无限循环
        std::cout << "请输入内容 (输入 'exit' 退出)：";
        std::getline(std::cin, input);

        if (input == "exit") {
            std::cout << "程序正在退出..." << std::endl;
            break; // 用户输入 exit 时退出循环
        }

        // 打印用户输入
        std::cout << "您输入的是: " << input << std::endl;

        // 获取并打印gem5的当前时钟周期
        uint64_t curTick = m5_cur_tick();
        std::cout << "当前gem5时钟周期: " << curTick << std::endl;
    }
    return 0;
}


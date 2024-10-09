#include <iostream>
#include <string>

int main() {
    std::string input;
    while (1) { // 无限循环
        std::cout << "请输入内容bb (输入 'exit' 退出)：";
        std::getline(std::cin, input);

        if (input == "exit") {
            std::cout << "程序正在退出...bb" << std::endl;
            break; // 用户输入 exit 时退出循环
        }

        std::cout << "您输入的是:bb " << input << std::endl;
    }
    return 0;
}


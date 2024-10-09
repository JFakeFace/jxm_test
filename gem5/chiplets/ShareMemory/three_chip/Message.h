#ifndef MESSAGE_H
#define MESSAGE_H

#include <iostream>
#include <fstream>
#include <cstring>
#include <sstream>

using namespace std;

typedef struct msg {
    int src_chip, dest_chip, next_chip;
    int x, y, data;
} Message;

void Send(Message msg) {
    ofstream file;
    int next_chip = msg.next_chip;
    string file_name = "message" + to_string(next_chip) + ".txt";
    file.open(file_name, ios::app);
    file << msg.src_chip << " " << msg.dest_chip << " " << msg.next_chip << " " << msg.x << " " << msg.y << " " << msg.data << endl;
    file.close();
}

long long gadia_last_position = 0;
Message Recv(int chip_id) {
    std::string fileName = "message";
    fileName += to_string(chip_id) + ".txt";
    std::ifstream file;
    file.open(fileName, ios::in);
    if (!file.is_open()) {
        std::cout << "Error: open file failed!" << std::endl;
        exit(1);
    }

    file.seekg(gadia_last_position);
    stringstream ss;
    std::string line = "";
    Message msg;
    if (getline(file, line)) {
        ss.clear();
        ss.str(line);
        ss >> msg.src_chip >> msg.dest_chip >> msg.next_chip >> msg.x >> msg.y >> msg.data;
        gadia_last_position = file.tellg();
        file.close();
        return msg;
    } else {
        cout << "the file is read over" << endl;
        file.close();
        return msg;
    }
}

#endif // MESSAGE_UTILS_H


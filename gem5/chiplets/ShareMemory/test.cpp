#include<iostream>
#include<fstream>
#include<cstring>
#include <sstream>
#include"Message.h"
using namespace std;

int main() {
    Message msg;
    msg.src_chip = 0;
    msg.dest_chip = 1;
    msg.next_chip = 1;
    msg.data = 100;
    Send(msg);
    msg.data = 101;
    Send(msg);
    Message recv_msg = Recv(1);
    cout << recv_msg.src_chip << " " << recv_msg.dest_chip << " " << recv_msg.next_chip << " " << recv_msg.data << endl;

    Message recv_msg2 = Recv(1);
    cout << recv_msg2.src_chip << " " << recv_msg2.dest_chip << " " << recv_msg2.next_chip << " " << recv_msg2.data << endl;

    recv_msg2 = Recv(1);
    Send(msg);
    recv_msg2 = Recv(1);
    cout << recv_msg2.src_chip << " " << recv_msg2.dest_chip << " " << recv_msg2.next_chip << " " << recv_msg2.data << endl;


    return 0;


}

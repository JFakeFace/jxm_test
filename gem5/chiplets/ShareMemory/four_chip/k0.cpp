#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "Message.h"
#include <vector>
#include <cstdlib> // for atoi
#include <cstdlib> // for exit
#include<cmath>
using namespace std;
int chip_num = 4;
int N = 8;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Error: Please provide a chip id as a command-line argument." << endl;
        return 1; // Returning 1 indicates an error
    }
    int cnt = 0;
    int chip_id = atoi(argv[1]);
    chip_num = atoi(argv[2]);
    N = atoi(argv[3]);
    if (chip_id == -1) {
        cout << "Error: Invalid chip id provided." << endl;
        exit(1);
    }
    vector<vector<int>> v1(N, vector<int>(N, 1));
    vector<vector<int>> v2(N, vector<int>(N, 1));
    vector<vector<int>> v3(N, vector<int>(N, 0));

    int rows_per_chip = N / chip_num;
    int remainder = N % chip_num;
    int start = chip_id < remainder ? chip_id * (rows_per_chip + 1) : chip_id * rows_per_chip + remainder;
    int end = start + (chip_id < remainder ? rows_per_chip + 1 : rows_per_chip);
    //cout << chip_id << " " << start << " " << end << endl;

    for (int i = start; i < end; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                v3[i][j] += v1[i][k] * v2[k][j];
            }
        }
    }

    ifstream file("message0");
    string line;
    long long last_position = 0;
    if (!file.is_open()) {
        cerr << "Failed to open the file." << endl;
        return -1;
    }

    while (1) {
      file.clear();  // 清除EOF标志和其他可能的错误状态
      file.seekg(last_position);
      while (getline(file, line)) {
          
          stringstream ss(line);
          Message msg;
          ss >> msg.src_chip >> msg.dest_chip >> msg.next_chip >> msg.x >> msg.y >> msg.data;
          //cout<<msg.src_chip<<" "<<msg.dest_chip<<" "<<msg.next_chip<<" "<<msg.x<<" "<<msg.y<<" "<<msg.data<<endl;
          if (msg.data == -2) {
              cnt++;
          } else {
              v3[msg.x][msg.y] += msg.data;
          }
          last_position = max(last_position, (long long )file.tellg());
          
      }
        if (cnt == chip_num - 1) {
          break;
        }
    
      cout << "last_position: " << last_position << endl;
    }

    file.close();

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            cout << v3[i][j] << " ";
       }
        cout << endl;
    }

    return 0;
}


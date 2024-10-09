#include <iostream>
#include <fstream>
#include <string>
#include "Message.h"
#include <vector>
#include <cstdlib> // for atoi
#include <cstdlib> // for exit

using namespace std;

const int N = 4;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Error: Please provide a chip id as a command-line argument." << endl;
        return 1; // Returning 1 indicates an error
    }
    
    int chip_id = atoi(argv[1]);
    if (chip_id == -1) {
        cout << "Error: Invalid chip id provided." << endl;
        exit(1);
    }

    vector<vector<int>> v1(N, vector<int>(N, 1));
    vector<vector<int>> v2(N, vector<int>(N, 1));
    vector<vector<int>> v3(N, vector<int>(N, 0));

    for (int i = N/2; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                v3[i][j] += v1[i][k] * v2[k][j];
            }
        }
    }

    while (true) {
        Message msg = Recv(chip_id);
        if (msg.data == -2) {
            break;
        } else {
            v3[msg.x][msg.y] += msg.data;
        }
    }

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            cout << v3[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}


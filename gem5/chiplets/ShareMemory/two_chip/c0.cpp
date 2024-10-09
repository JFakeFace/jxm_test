#include<iostream>
#include<fstream>
#include<string>
#include"Message.h"
#include<vector>

using namespace std;

const int N = 4;

int main(int argc, char** argv) {
    int chip_id = -1;
    if (argc < 2) {
        cout << "Error: Please provide a chip id as a command-line argument." << endl;
        return 1; // Returning 1 indicates an error
    }
    chip_id = atoi(argv[1]);
    if (chip_id == -1) {
        cout << "Error: Invalid chip id provided." << endl;
        return 1; // Returning 1 indicates an error
    }
    vector<vector<int>> v1(N, vector<int>(N, 1));
    vector<vector<int>> v2(N, vector<int>(N, 1));
    vector<vector<int>> v3(N, vector<int>(N, 0));

    for (int i = 0; i < N / 2; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                v3[i][j] += v1[i][k] * v2[k][j];
            }
        }
    }

    for (int i = 0; i < N / 2; i++) {
        for (int j = 0; j < N; j++) {
            Send(Message{ chip_id, 1, 1, i, j, v3[i][j] });
        }
    }
    Send(Message{ chip_id, 1, 1, -1, -1, -2 });
    return 0;
}


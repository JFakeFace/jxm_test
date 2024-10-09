#include<iostream>
#include<fstream>
#include<string>
#include"Message.h"
#include<vector>
using namespace std;
int N = 8;
int chip_num = 4;
int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Error: Please provide a chip id as a command-line argument." << endl;
        return 1; // Returning 1 indicates an error
    }

    int chip_id = atoi(argv[1]);
    chip_num = atoi(argv[2]);
    N = atoi(argv[3]);
    if (chip_id == -1) {
        cout << "Error: Invalid chip id provided." << endl;
        exit(1);
    }
    vector<vector<int>>v1(N,vector<int>(N,1));
    vector<vector<int>>v2(N,vector<int>(N,1));
    vector<vector<int>>v3(N,vector<int>(N,0));

	int rows_per_chip = N / chip_num;
	int remainder = N % chip_num;
	int start = chip_id < remainder ? chip_id * (rows_per_chip + 1) : chip_id * rows_per_chip + remainder;
	int end = start + (chip_id < remainder ? rows_per_chip + 1 : rows_per_chip);

  // cout<<chip_id<<" "<<start<<" " << end << endl;

  ofstream file("message0",ios::app);
    for (int i = start; i < end; i++) {
        for(int j = 0;j < N;j++) {  
            for(int k = 0;k < N;k++) {
                v3[i][j] += v1[i][k] * v2[k][j];
            }
	          file << chip_id << " " << 0 << " " << 0 << " " << i << " " << j << " " << v3[i][j] << endl;
        }

    }
    file << chip_id << " " << 0 << " " << 0 << " " << -1 << " " << -1 << " " << -2 << endl;
    file.close();
    return 0;
}

#include <iostream>
#include <mpi.h>
#include <cstdlib> // For atoi()

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Assume the second argument is chipid, the third is chipnum (total chips), and the fourth is N
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " chipid chipnum N\n";
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int chipid = atoi(argv[1]);
    int chipnum = atoi(argv[2]);
    int N = atoi(argv[3]);

    if (world_rank == chipid) {
        int number = N;  // Example use of N
        // Assuming sending to the next chipid in a simple circular manner
        int target = (chipid + 1) % chipnum;
        MPI_Send(&number, 1, MPI_INT, target, 0, MPI_COMM_WORLD);
        std::cout << "Process " << chipid << " sent number " << number << " to Process " << target << std::endl;
    }

    MPI_Finalize();
    return 0;
}


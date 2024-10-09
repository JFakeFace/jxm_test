#include <iostream>
#include <mpi.h>
#include <cstdlib> // For atoi()

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_rank, world_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " chipid chipnum N\n";
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int chipid = atoi(argv[1]);
    int chipnum = atoi(argv[2]);
    int N = atoi(argv[3]);

    if (world_rank == chipid) {
        int number;
        // Assuming receiving from the previous chipid in a simple circular manner
        int source = (chipid - 1 + chipnum) % chipnum;
        MPI_Recv(&number, 1, MPI_INT, source, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        std::cout << "Process " << chipid << " received number " << number << " from Process " << source << std::endl;
    }

    MPI_Finalize();
    return 0;
}


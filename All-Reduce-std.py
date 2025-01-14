from mpi4py import MPI
import numpy as np


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    data = None
    base_value = rank * size
    data = np.arange(base_value, base_value + size, dtype=int)

    result = comm.allreduce(data, MPI.SUM)

    # Print the result
    print(f"Process {rank}, result: {result}")

if __name__ == "__main__":
    main()

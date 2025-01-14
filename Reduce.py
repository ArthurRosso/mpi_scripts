from mpi4py import MPI
import numpy as np

def standard_reduce(comm, rank, size, data):
    return comm.reduce(data)

def reduce(comm, rank, size, data, root=0):
    buffer = np.array([data], dtype='i')
    for c in range(2):
        n = (rank+1)*2-c
        if n < size:
            buf = np.empty_like(buffer)
            comm.Recv(buf=buf, source=n, tag=11)
            buffer += buf
    if rank != root:
        root = (rank + (0 if rank % 2 == 0 else 1)) // 2 - 1
        comm.Send(buf=buffer, dest=root, tag=11)
        return None
    else:
        return buffer[0]

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    data = rank  # Each process has its own data
    reduced_data = reduce(comm, rank, size, data)

    if rank == 0:
        print(f"Root process reduced data: {reduced_data}")

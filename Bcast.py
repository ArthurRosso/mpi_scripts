from mpi4py import MPI
import numpy as np

def standard_bcast(comm, rank, size, data):
    return comm.bcast(data, root=0)

def bcast_v1(comm, rank, size, data):
    buffer = np.array([data], dtype='i') if rank == 0 else np.empty(1, dtype='i')
    if rank == 0:
        for i in range(1,4):
            comm.Send(buf=buffer, dest=i, tag=11)
    else:
        comm.Recv(buf=buffer, source=0, tag=11)
    return buffer[0]

def bcast_v2(comm, rank, size, data):
    buffer = np.array([data], dtype='i') if rank == 0 else np.empty(1, dtype='i')
    if rank == 0:
        # print(buf)
        for i in range(1,3):
            comm.Send(buf=buffer, dest=i, tag=11)
    else:
        root = (rank + (0 if rank % 2 == 0 else 1)) // 2 - 1
        comm.Recv(buf=buffer, source=root, tag=11)
        if (rank+1)*2 < size:
            comm.Send(buf=buffer, dest=(rank+1)*2, tag=11)
        if (rank+1)*2-1 < size:
            comm.Send(buf=buffer, dest=(rank+1)*2-1, tag=11)
    # print(data)
    return buffer[0]

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    data = 42 if rank == 0 else None

    # result = standard_bcast(comm, data)
    result = bcast_v2(comm, rank, size, data)

    if result is not None:
        print(f"Process {rank}: broadcasted data = {result}")

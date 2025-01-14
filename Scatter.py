from gc import collect
from mpi4py import MPI
import numpy as np

def standard_scatter(comm, rank, size, data):
    return comm.scatter(data, root=0)


def parent(rank):
    return (rank + (0 if rank % 2 == 0 else 1)) // 2 - 1

def get_id(parent, child):
    return (parent+1)*2-(1-child)

def scatter(comm, rank, size, data, root=0):
    for c in range(2):
        buf.clear()

        collect(get_id(o, c), buf, data)
        send(buf, dest=get_id(rank, c), tag=11)

def collect(root, buf, data):
    if root < size:
        q = []
        q.push(root)
        while q.size() > 0:
            pending = q.size()
            while pending > 0
            next = q.pop()
            buf.apend(data[next])
            for c in range(2):
                i = get_id(next, c)
                if i < size:
                    q.push(i)
                else:
                    break
            pending -= 1

def scatter(comm, rank, size, data, root=0):
    """Scatter data from the root process to all processes."""
    if rank == root:
        for c in range(2):
            child_rank = get_id(rank, c)
            if child_rank < size:
                comm.send(data[child_rank], dest=child_rank, tag=11)
    else:
        received_data = comm.recv(source=parent(rank), tag=11)
        print(f"Rank {rank} received data: {received_data}")

def collect(comm, rank, size, data, root=0):
    """Collect data from all processes back to the root process."""
    if rank != root:
        comm.send(data[rank], dest=parent(rank), tag=12)
    else:
        buffer = [data[root]]
        for c in range(2):
            child_rank = get_id(rank, c)
            if child_rank < size:
                received_data = comm.recv(source=child_rank, tag=12)
                buffer.append(received_data)
        print(f"Root collected data: {buffer}")

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # data = np.array([0, 1, 2, 3])
    # scattered_data = standard_scatter(comm, rank, size, data)


    # data = np.array([0, 1, 2, 3])
    # scattered_data = standard_scatter(comm, rank, size, data)
    if rank == 0:
        data = np.array([0, 1, 2, 3])
    else
        data = None

    if scattered_data is not None:
        print(f"Process {rank}: scattered data: {scattered_data}")







# from mpi4py import MPI
# import numpy as np

# comm = MPI.COMM_WORLD
# myrank = comm.Get_rank()
# commsize = comm.Get_size()

# # if myrank == 0:
# #     data = [(i+1)**2 for i in range(commsize)]
# # else:
# #     data = None
# # data = comm.scatter(data, root=0)
# # assert data == (myrank+1)**2

# if myrank == 0:
#     for i in range(1, commsize):
#         comm.send((i+1)**2, dest=i, tag=11)
#     data = (myrank+1)**2
# else:
#     data = comm.recv(source=0, tag=11)
# assert data == (myrank+1)**2

# def scatter():
#     parent = (rank + (0 if  rank % 2 == 0 else 1)) / 2 - 1
#     if rank != 0:
#         buf = comm.recv(source=parent, tag=11)
#     else:
#         data = [A, B, C, D]
#     for i in range(2):
#         buf = None
#         buf += data[(rank+1)*2-i)]
#         collect((rank+1)*2-i)), buf, data)
#         comm.send(buf, dest=i, tag=11)

# def collect(root, buffer, data):
#     if root < size:
#         for i in range(2):
#             checked_concat((root+1)*2-i)), buffer, data)
#         for i in range(2):
#             collect((root+1)*2-i)), buffer, data)

# def checked_concat(root, buffer, data):
#     if root < size:
#         buffer += data[root]

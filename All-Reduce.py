from mpi4py import MPI
import numpy as np


def standard_allreduce(comm, sendbuf):
    return comm.allreduce(sendbuf, MPI.SUM)


# Short messages
def allreduce_reduce_broadcast(comm, rank, size, sendbuf, op):
    # Perform the reduction
    recvbuf = comm.reduce(sendbuf)

    # Broadcast the result
    recvbuf = comm.bcast(recvbuf, root=0)

    return recvbuf


# Long messages
# Reduce-scatter followed by Allgather
def allreduce_RS_GA(comm, rank, size, sendbuf, op):
    # Perform the reduction
    recvbuf = comm.reduce(sendbuf)

    # Perform the scatter
    recvbuf = comm.scatter([recvbuf]*size)

    # Perform the allgather
    recvbuf = comm.allgather(recvbuf)

    return recvbuf



def allreduce_radix_k(comm, rank, size, data, rounds):
    group_size = size
    for r, k_i in enumerate(rounds):
        group_size = group_size // k_i
        if group_size == 1:
            base = (rank // k_i) * k_i
            dst_list = [base + i for i in range(k_i)]
        else:
            base = rank % (size // k_i)
            dst_list = [base + i * group_size for i in range((size - base + group_size - 1) // group_size)]
        for dst_index, dst in enumerate(dst_list):
            if dst != rank:
                if group_size == 1:
                    start = dst
                    end = dst + 1
                else:
                    start = dst_index * group_size
                    end = start + group_size
                comm.send(data[start:end], dest=dst, tag=r)
                received_data = comm.recv(source=dst, tag=r)
                if group_size == 1:
                    start = rank
                    end = start + 1
                else:
                    partition_index = int(rank // (size / k_i))
                    part_size = size // k_i
                    remainder = size % k_i
                    start = partition_index * part_size + min(partition_index, remainder)
                    end = start + len(received_data) #+ part_size #+ (1 if partition_index < remainder else 0)
                c = 0
                for i in range(start, end):
                    data[i] += received_data[c]
                    c+=1

    gathered_data = comm.allgather(data[rank].item())
    return gathered_data

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # # Each process has a buffer of size 1
    # sendbuf = rank+1
    # print(f"Process {rank}, sendbuf: {sendbuf}")

    # # Perform the all-reduce operation

    # # result = allreduce_reduce_broadcast(comm, rank, size, sendbuf, op)

    # # result = allreduce_RS_GA(comm, rank, size, sendbuf, op)

    data = None
    # if rank == 0:
    #     data = np.arange(6, dtype=int)
    # elif rank == 1:
    #     data = np.arange(6, 12, dtype=int)
    # elif rank == 2:
    #     data = np.arange(12, 18, dtype=int)
    # elif rank == 3:
    #     data = np.arange(18, 24, dtype=int)
    # elif rank == 4:
    #     data = np.arange(24, 30, dtype=int)
    # elif rank == 5:
    #     data = np.arange(30, 36, dtype=int)

    # if rank == 0:
    #     data = np.arange(4, dtype=int)
    # elif rank == 1:
    #     data = np.arange(4, 8, dtype=int)
    # elif rank == 2:
    #     data = np.arange(8, 12, dtype=int)
    # elif rank == 3:
    #     data = np.arange(12, 16, dtype=int)
    base_value = rank * size
    data = np.arange(base_value, base_value + size, dtype=int)

    # result = standard_allreduce(comm, data)

    rounds = [3,2]
    result = allreduce_radix_k(comm, rank, size, data, rounds)

    # Print the result
    print(f"Process {rank}, result: {result}")

if __name__ == "__main__":
    main()

# from mpi4py import MPI
# import numpy as np

# def reduce_scatter_v0(comm, rank, size, data, rounds):
#     # Validate decomposition of p
#     if np.prod(rounds) != size:
#         raise ValueError("The product of factors must equal the total number of processes.")

#     # Initialize local data and ensure consistency of data shape across processes
#     # if rank == 0:
#     #     if len(data) % size != 0:
#     #         raise ValueError("Array size must be divisible by the number of processes.")

#     # data = comm.bcast(data if rank == 0 else None, root=0)

#     # Start with the full data array
#     # recvbuf = np.array_split(data, size)[rank]

#     # # Perform the reduction across rounds
#     # for i, k_i in enumerate(rounds):

#     # Round 0:
#     if rank == 0:
#         sendbuf = data[1::2]
#         comm.send(sendbuf, dest=1, tag=0)
#         recvbuf = comm.recv(source=1, tag=0)
#         data[0::2] += recvbuf
#     elif rank == 1:
#         recvbuf = comm.recv(source=0, tag=0)
#         data[1::2] += recvbuf
#         sendbuf = data[0::2]
#         comm.send(sendbuf, dest=0, tag=0)
#     elif rank == 2:
#         sendbuf = data[1::2]
#         comm.send(sendbuf, dest=3, tag=0)
#         recvbuf = comm.recv(source=3, tag=0)
#         data[0::2] += recvbuf
#     elif rank == 3:
#         recvbuf = comm.recv(source=2, tag=0)
#         data[1::2] += recvbuf
#         sendbuf = data[0::2]
#         comm.send(sendbuf, dest=2, tag=0)

#     print("Round 0: ok")

#     # Round 1:
#     if rank == 0:
#         sendbuf = data[2]
#         comm.send(sendbuf, dest=2, tag=1)
#         recvbuf = comm.recv(source=2, tag=1)
#         data[0] += recvbuf
#     elif rank == 1:
#         sendbuf = data[3]
#         comm.send(sendbuf, dest=3, tag=1)
#         recvbuf = comm.recv(source=3, tag=1)
#         data[1] += recvbuf
#     elif rank == 2:
#         recvbuf = comm.recv(source=0, tag=1)
#         data[2] += recvbuf
#         sendbuf = data[0]
#         comm.send(sendbuf, dest=0, tag=1)
#     elif rank == 3:
#         recvbuf = comm.recv(source=1, tag=1)
#         data[3] += recvbuf
#         sendbuf = data[1]
#         comm.send(sendbuf, dest=1, tag=1)

#     print("Round 1: ok")
#     return data[rank]

# def reduce_scatter_v1(comm, rank, size, data, rounds):
#     # Validate decomposition of p
#     if np.prod(rounds) != size:
#         raise ValueError("The product of factors must equal the total number of processes.")

#     # Round 0:
#     r = 0
#     k_i = rounds[r]
#     group_size = len(data)//k_i
#     if rank == 0:
#         recvbuf = comm.recv(source=2, tag=r)
#         comm.send(data[group_size:len(data)], dest=2, tag=r)
#         data[0:group_size] += recvbuf
#     elif rank == 1:
#         recvbuf = comm.recv(source=3, tag=r)
#         comm.send(data[group_size:len(data)], dest=3, tag=r)
#         data[0:group_size] += recvbuf
#     elif rank == 2:
#         comm.send(data[0:group_size], dest=0, tag=r)
#         recvbuf = comm.recv(source=0, tag=r)
#         data[group_size:len(data)] += recvbuf
#     elif rank == 3:
#         comm.send(data[0:group_size], dest=1, tag=r)
#         recvbuf = comm.recv(source=1, tag=r)
#         data[group_size:len(data)] += recvbuf

#     # print(f"Round {r} process {rank}: ok")

#     # Round 1:
#     r = 1
#     k_i = rounds[r]
#     group_size = group_size//k_i
#     if rank == 0:
#         comm.send(data[1:2], dest=1, tag=r)
#         recvbuf = comm.recv(source=1, tag=r)
#         data[0] += recvbuf[0]
#     elif rank == 1:
#         recvbuf = comm.recv(source=0, tag=r)
#         comm.send(data[0:1], dest=0, tag=r)
#         data[1] += recvbuf[0]
#     elif rank == 2:
#         comm.send(data[3:4], dest=3, tag=r)
#         recvbuf = comm.recv(source=3, tag=r)
#         data[2] += recvbuf[0]
#     elif rank == 3:
#         recvbuf = comm.recv(source=2, tag=r)
#         comm.send(data[2:3], dest=2, tag=r)
#         data[3] += recvbuf[0]

#     # print(f"Round 0 process {rank}: ok")
#     return data[rank]


# # def reduce_scatter(comm, rank, size, data, rounds):
# #     # Validate decomposition of p
# #     if np.prod(rounds) != size:
# #         raise ValueError("The product of factors must equal the total number of processes.")

# #     group_size = len(data)

# #     for r, k_i in enumerate(rounds):
# #         # Calculate the size of each group for the current round
# #         group_size //= k_i

# #         # Determine source and destination processes for communication
# #         source = (rank + k_i) % size
# #         dest = (rank - k_i) % size

# #         if rank % k_i < k_i // 2:
# #             # Send data to the paired process and receive data from it
# #             comm.send(data[group_size:], dest=dest, tag=r)
# #             recvbuf = comm.recv(source=source, tag=r)
# #             data[:group_size] += recvbuf
# #         else:
# #             # Receive data from the paired process and send data to it
# #             recvbuf = comm.recv(source=source, tag=r)
# #             comm.send(data[:group_size], dest=dest, tag=r)
# #             data[group_size:] += recvbuf

# #     return data[rank]
# def reduce_scatter(comm, rank, size, data, rounds):
#     # Validate decomposition of p
#     if np.prod(rounds) != size:
#         raise ValueError("The product of factors must equal the total number of processes.")

#     group_size = len(data)

#     for r, k_i in enumerate(rounds):
#         # Calculate the size of each group for the current round
#         group_size //= k_i

#         # Determine the local group the process belongs to
#         group_id = rank // (size // k_i)

#         for i in range(size // k_i):
#             paired_rank = group_id * (size // k_i) + (i + group_id + 1) % (size // k_i)

#             if rank == group_id * (size // k_i) + i:
#                 # Send data to the paired process and receive data from it
#                 comm.send(data[group_size * i: group_size * (i + 1)], dest=paired_rank, tag=r)
#                 recvbuf = comm.recv(source=paired_rank, tag=r)
#                 data[group_size * i: group_size * (i + 1)] += recvbuf

#             elif rank == paired_rank:
#                 # Receive data from the original process and send data back
#                 recvbuf = comm.recv(source=group_id * (size // k_i) + i, tag=r)
#                 comm.send(data[group_size * i: group_size * (i + 1)], dest=group_id * (size // k_i) + i, tag=r)
#                 data[group_size * i: group_size * (i + 1)] += recvbuf

#     return data[rank]


#     return data[rank]
# def reduce_scatter_vtest(comm, rank, size, data, rounds):
#     # Validate decomposition of p
#     if np.prod(rounds) != size:
#         raise ValueError("The product of factors must equal the total number of processes.")

#     # Round 0:
#     group_size = len(data)

#     for r, k_i in enumerate(rounds):
#         group_size //= k_i

#         for i in range(k_i-1):
#             if rank == 0:
#                 recvbuf = comm.recv(source=group_size+i, tag=r)
#                 comm.send(data[group_size:len(data)], dest=2, tag=r)
#                 data[0:group_size] += recvbuf
#             elif rank == 1:
#                 recvbuf = comm.recv(source=3, tag=r)
#                 comm.send(data[group_size:len(data)], dest=3, tag=r)
#                 data[0:group_size] += recvbuf
#             elif rank == 2:
#                 comm.send(data[0:group_size], dest=0, tag=r)
#                 recvbuf = comm.recv(source=0, tag=r)
#                 data[group_size:len(data)] += recvbuf
#             elif rank == 3:
#                 comm.send(data[0:group_size], dest=1, tag=r)
#                 recvbuf = comm.recv(source=1, tag=r)
#                 data[group_size:len(data)] += recvbuf

#     # print(f"Round {r} process {rank}: ok")

#     # # Round 1:
#     # if rank == 0:
#     #     comm.send(data[1:2], dest=1, tag=r)
#     #     recvbuf = comm.recv(source=1, tag=r)
#     #     data[0] += recvbuf[0]
#     # elif rank == 1:
#     #     recvbuf = comm.recv(source=0, tag=r)
#     #     comm.send(data[0:1], dest=0, tag=r)
#     #     data[1] += recvbuf[0]
#     # elif rank == 2:
#     #     comm.send(data[3:4], dest=3, tag=r)
#     #     recvbuf = comm.recv(source=3, tag=r)
#     #     data[2] += recvbuf[0]
#     # elif rank == 3:
#     #     recvbuf = comm.recv(source=2, tag=r)
#     #     comm.send(data[2:3], dest=2, tag=r)
#     #     data[3] += recvbuf[0]

#     # print(f"Round 0 process {rank}: ok")
#     return data[rank]

# if __name__ == "__main__":
#     comm = MPI.COMM_WORLD
#     rank = comm.Get_rank()
#     size = comm.Get_size()

#     # Example array and decomposition of p
#     # data = None
#     # if rank == 0:
#     #     data = np.arange(16, dtype=int)  # Example array
#     # data = np.array([rank*4+0, rank*4+1, rank*4+2, rank*4+3], dtype=int)
#     # round = [2,2]  # Example decomposition, must multiply to `size`

#     # Perform reduce-scatter
#     # result = reduce_scatter(comm, rank, size, data, round)

#     data = None

#     if rank == 0:
#         data = np.arange(4, dtype=int)
#     elif rank == 1:
#         data = np.arange(4, 8, dtype=int)
#     elif rank == 2:
#         data = np.arange(8, 12, dtype=int)
#     elif rank == 3:
#         data = np.arange(12, 16, dtype=int)

#     result = comm.allreduce(data)

#     print(f"Process {rank} result: {result}")

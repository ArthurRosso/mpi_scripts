from mpi4py import MPI
import numpy as np

def gather_to_all(comm, rank, size, data):
    next = (rank+1) % size
    prev = (rank-1) % size

    buf1 = data
    buf2 = buf1
    gathered_data = np.array([], dtype=int)

    if rank % 2 == 0:
        for i in range(size-1):
            print(f"Rank: {rank}, msg: {buf1}, dest: {next}")
            comm.Send(buf1, dest=next, tag=11)
            gathered_data = np.append(gathered_data,buf1)
            print(f"Rank: {rank}, Data: {gathered_data}")
            print(f"Rank: {rank}, msg: {buf1}, source: {prev}")
            comm.Recv(buf1, source=prev, tag=11)
    else:
        gathered_data = np.append(gathered_data,buf1)
        print(f"Rank: {rank}, Data: {gathered_data}")
        for i in range(size-1):
            print(f"Rank: {rank}, msg: {buf1}, source: {prev}")
            comm.Recv(buf1, source=prev, tag=11)
            gathered_data = np.append(gathered_data,buf1)
            print(f"Rank: {rank}, Data: {gathered_data}")
            print(f"Rank: {rank}, msg: {buf2}, dest: {next}")
            comm.Send(buf2, dest=next, tag=11)
            buf2 = buf1

    return gathered_data


def gather_to_all_binary_swap(comm, rank, size, data):
    # Each process starts with its own data
    gathered_data = np.array(data, dtype=np.float64)

    step = 1
    while step < size:
        partner = rank ^ step

        # Send current data to partner and receive partner's data
        send_buf = gathered_data.copy()
        recv_buf = np.empty_like(gathered_data)

        comm.Send(send_buf, dest=partner)
        comm.Recv(recv_buf, source=partner)

        # Merge received data with local data
        gathered_data = np.concatenate((gathered_data, recv_buf))
        step *= 2

    # All processes now have the gathered data
    return gathered_data


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Initialize each process's data
    # data = np.array([rank], dtype=np.float64)
    # data = None

    data = np.array([rank], dtype=int)
    print(data)
    # Perform the gather-to-all algorithm
    result = gather_to_all(comm, rank, size, data)

    if result is not None:
        print(f"Process {rank}: allgathered data = {result}")

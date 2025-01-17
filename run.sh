# mpiexec -n 4 python -m mpi4py Reduce.py
time mpiexec -n 6 python -m mpi4py All-Reduce-std.py
time mpiexec -n 6 python -m mpi4py All-Reduce.py

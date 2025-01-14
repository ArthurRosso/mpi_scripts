Results

Standard AllReduce:
Process 0, result: [24 28 32 36]
Process 2, result: [24 28 32 36]
Process 3, result: [24 28 32 36]
Process 1, result: [24 28 32 36]

real	0m0.307s
user	0m0.556s
sys	0m0.106s

Radix-k AllReduce:
Process 3, result: [24, 28, 32, 36]
Process 0, result: [24, 28, 32, 36]
Process 2, result: [24, 28, 32, 36]
Process 1, result: [24, 28, 32, 36]

real	0m0.268s
user	0m0.551s
sys	0m0.080s

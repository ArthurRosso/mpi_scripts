Results PC

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


Results grid5000

real	0m2.462s
user	0m0.854s
sys	0m2.504s


real	0m2.308s
user	0m0.678s
sys	0m2.575s

Process 1, result: [ 90  96 102 108 114 120]
Process 5, result: [ 90  96 102 108 114 120]
Process 3, result: [ 90  96 102 108 114 120]
Process 0, result: [ 90  96 102 108 114 120]
Process 2, result: [ 90  96 102 108 114 120]
Process 4, result: [ 90  96 102 108 114 120]

real	0m0.713s
user	0m0.776s
sys	0m0.157s
Process 1, result: [90, 96, 102, 108, 114, 120]
Process 2, result: [90, 96, 102, 108, 114, 120]
Process 0, result: [90, 96, 102, 108, 114, 120]
Process 3, result: [90, 96, 102, 108, 114, 120]
Process 5, result: [90, 96, 102, 108, 114, 120]
Process 4, result: [90, 96, 102, 108, 114, 120]

real	0m0.234s
user	0m0.702s
sys	0m0.093s

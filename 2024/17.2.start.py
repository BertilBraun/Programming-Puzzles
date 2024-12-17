# run:
# gcc -3 -o 17.2 17.2.c
# run in parallel

# MIN_ITER = 1_922_000_000
# MAX_ITER = 10_000_000_000_000
# PROGRAMS = 8
# PORTION = (MAX_ITER - MIN_ITER) // PROGRAMS
# for i in range(8)
# Start ./17.2 MIN_ITER + PORTION * i MIN_ITER + PORTION * (i + 1)
# Wait for all to finish

import os
from subprocess import Popen

MIN_ITER = 2298000000
MAX_ITER = 10_000_000_000_000
PROGRAMS = 8
PORTION = (MAX_ITER - MIN_ITER) // PROGRAMS


os.system('gcc -O3 -o 17.2 17.2.c')

for i in range(PROGRAMS):
    Popen(['./17.2', str(MIN_ITER + PORTION * i), str(MIN_ITER + PORTION * (i + 1))])
    print(f'Started {i}')
    os.system('sleep 1')

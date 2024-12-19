#!/usr/bin/env python3

import time

begin_time = time.time()
from solver import *
import_time = time.time() - begin_time

print("Import time:", import_time)

def assert_equals(a, b, clues):
    a = list(list(row) for row in a)
    b = list(list(row) for row in b)
    if not all(row == expected_row for row, expected_row in zip(a, b)):
        print('Failed!')
        print_board(a, clues)
        print('Expected:')
        print_board(b, clues)
        exit(1)
    print('Passed!')


# expected = [
#     [2, 1, 4, 3],
#     [3, 4, 1, 2],
#     [4, 2, 3, 1],
#     [1, 3, 2, 4],
# ]
# clues = [0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0]
# res = solve_puzzle(clues, 4)
# print(res)
# assert_equals(res, expected, clues)

# expected = [
#     [5, 6, 1, 4, 3, 2],
#     [4, 1, 3, 2, 6, 5],
#     [2, 3, 6, 1, 5, 4],
#     [6, 5, 4, 3, 2, 1],
#     [1, 2, 5, 6, 4, 3],
#     [3, 4, 2, 5, 1, 6],
# ]
# clues = [0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0]
# res = solve_puzzle(clues, 6)
# print(res)
# assert_equals(res, expected, clues)


def timed_solve(clues, size):
    start = time.time()
    res = solve_puzzle(clues, size)
    print('Time:', time.time() - start)
    return res


expected = [
[1, 5, 6, 7, 4, 3, 2],
[2, 7, 4, 5, 3, 1, 6],
[3, 4, 5, 6, 7, 2, 1],
[4, 6, 3, 1, 2, 7, 5],
[5, 3, 1, 2, 6, 4, 7],
[6, 2, 7, 3, 1, 5, 4],
[7, 1, 2, 4, 5, 6, 3],
]
clues = [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]
assert_equals(timed_solve(clues, 7), expected, clues)

clues = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]
assert_equals(
timed_solve(clues, 7),  # for a _very_ hard puzzle, replace the last 7 values with zeroes
[
    [7, 6, 2, 1, 5, 4, 3],
    [1, 3, 5, 4, 2, 7, 6],
    [6, 5, 4, 7, 3, 2, 1],
    [5, 1, 7, 6, 4, 3, 2],
    [4, 2, 1, 3, 7, 6, 5],
    [3, 7, 6, 2, 1, 5, 4],
    [2, 4, 3, 5, 6, 1, 7],
],
clues,
)

clues = [0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3]
assert_equals(
timed_solve(clues, 7),
[
    [3, 4, 1, 7, 6, 5, 2],
    [7, 1, 2, 5, 4, 6, 3],
    [6, 3, 5, 2, 1, 7, 4],
    [1, 2, 3, 6, 7, 4, 5],
    [5, 7, 6, 4, 2, 3, 1],
    [4, 5, 7, 1, 3, 2, 6],
    [2, 6, 4, 3, 5, 1, 7],
],
clues,
)

print("Real test")
begin_time = time.time()

clues = [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]
print("Medium")
timed_solve(clues, 7)
clues =  [6, 4, 0, 2, 0, 0, 3, 0, 3, 3, 3, 0, 0, 4, 0, 5, 0, 5, 0, 2, 0, 0, 0, 0, 4, 0, 0, 3]
print("Hard")
timed_solve(clues, 7)
clues =  [0, 0, 0, 5, 0, 0, 3, 0, 6, 3, 4, 0, 0, 0, 3, 0, 0, 0, 2, 4, 0, 2, 6, 2, 2, 2, 0, 0]
print("Hard")
timed_solve(clues, 7)
clues =  [0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3]
print("Very Hard")
timed_solve(clues, 7)
clues = [0, 0, 5, 3, 0, 2, 0, 0, 0, 0, 4, 5, 0, 0, 0, 0, 0, 3, 2, 5, 4, 2, 2, 0, 0, 0, 0, 5]
print("Very Hard")
timed_solve(clues, 7)
clues = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1]
print("Very Hard")
timed_solve(clues, 7)
clues = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]
timed_solve(clues, 7)
print("Medved")
clues = [3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]
timed_solve(clues, 7)
print("Time:", time.time() - begin_time + import_time)

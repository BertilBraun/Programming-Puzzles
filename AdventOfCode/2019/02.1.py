from aoc import *
from util import *

DAY = 2
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day=2)
else:
    input = get_input(day=2)


def solve(input: str) -> str | int:
    prog = [int(x) for x in input.split(',')]
    prog[1] = 12
    prog[2] = 2
    i = 0
    while prog[i] != 99:
        if prog[i] == 1:
            prog[prog[i + 3]] = prog[prog[i + 1]] + prog[prog[i + 2]]
        elif prog[i] == 2:
            prog[prog[i + 3]] = prog[prog[i + 1]] * prog[prog[i + 2]]
        else:
            raise Exception(f'Invalid opcode: {prog[i]}')
        i += 4

    return prog[0]


if EXAMPLE:
    print(solve(input))
else:
    submit(day=2, part=1, answer=solve(input))

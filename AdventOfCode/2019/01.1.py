from aoc import *
from util import *

DAY = 1
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day=1)
else:
    input = get_input(day=1)


def solve(input: str) -> str | int:
    ints = parse_ints(input)

    return sum(mass // 3 - 2 for mass in ints)


if EXAMPLE:
    print(solve(input))
else:
    submit(day=1, part=1, answer=solve(input))

from aoc import *
from util import *
from intcode import *

DAY = 5
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day=5)
else:
    input = get_input(day=5)


def solve(input: str) -> str | int:
    prog = parse_intcode(input)
    output = run_intcode(prog, [5])
    return output[-1]


if EXAMPLE:
    print(solve(input))
else:
    submit(day=5, part=2, answer=solve(input))

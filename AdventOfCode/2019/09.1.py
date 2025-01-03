from aoc import *
from util import *
from intcode import *

DAY = 9
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = """109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"""
else:
    input = get_input(day=9)


def solve(input: str) -> str | int | None:
    computer = Computer(input, [1])
    while not computer.done():
        res = computer.run(None)
        print(res)
    assert res and res > 203
    return res


if EXAMPLE:
    print(solve(input))
else:
    submit(day=9, part=1, answer=solve(input))

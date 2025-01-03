from aoc import *
from util import *
from intcode import *

DAY = 7
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = """3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"""
else:
    input = get_input(day=7)


def solve(input: str) -> str | int:
    answer = 0
    for perm in permutations(range(5), 5):
        res = 0
        for p in perm:
            computer = Computer(input, [p])
            res = computer.run(res)
            assert res is not None, 'No output from computer'
        answer = max(answer, res)

    return answer


if EXAMPLE:
    print(solve(input))
else:
    submit(day=7, part=1, answer=solve(input))

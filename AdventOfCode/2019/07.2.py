from aoc import *
from util import *
from intcode import *

DAY = 7
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = """3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"""
else:
    input = get_input(day=7)


def solve(input: str) -> str | int:
    answer = 0
    for perm in permutations(range(5, 10), 5):
        res = 0

        computers = [Computer(input, [p]) for p in perm]
        while not computers[-1].done():
            for computer in computers:
                res = computer.run(res)
                assert res is not None, 'No output from computer'

        answer = max(answer, res)

    return answer


if EXAMPLE:
    print(solve(input))
else:
    submit(day=7, part=2, answer=solve(input))

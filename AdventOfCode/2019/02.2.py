from aoc import *
from util import *
from intcode import *

DAY = 2
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day=2)
else:
    input = get_input(day=2)


def solve(input: str) -> str | int:
    prog = parse_intcode(input)
    for noun in range(100):
        for verb in range(100):
            prog[1] = noun
            prog[2] = verb
            ans = run_intcode(prog)
            if ans[0] == 19690720:
                return 100 * noun + verb

    assert False, 'No solution found'


if EXAMPLE:
    print(solve(input))
else:
    submit(day=2, part=2, answer=solve(input))

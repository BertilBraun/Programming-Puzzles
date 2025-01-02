from aoc import *
from util import *

DAY = 4
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day=4)
else:
    input = '264360-746325'


def solve(input: str) -> str | int:
    low, high = [int(x) for x in input.split('-')]

    num_valid_codes = 0
    for code in range(low, high + 1):
        code_str = str(code)
        if code_str != ''.join(sorted(code_str)):
            continue
        if not any(code_str[i] == code_str[i + 1] for i in range(5)):
            continue
        num_valid_codes += 1

    return num_valid_codes


if EXAMPLE:
    print(solve(input))
else:
    submit(day=4, part=1, answer=solve(input))

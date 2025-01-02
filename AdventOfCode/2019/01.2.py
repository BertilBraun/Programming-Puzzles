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

    def fuel(mass: int) -> int:
        if mass <= 0:
            return 0
        fuel_mass = max(mass // 3 - 2, 0)
        return fuel_mass + fuel(fuel_mass)

    return sum(fuel(mass) for mass in ints)


if EXAMPLE:
    print(solve(input))
else:
    submit(day=1, part=2, answer=solve(input))

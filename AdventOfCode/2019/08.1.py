from aoc import *
from util import *

DAY = 8
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day=8)
else:
    input = get_input(day=8)


def solve(input: str) -> str | int:
    W, H = 25, 6

    vals = [int(x) for x in input.strip()]
    layers = [vals[i : i + W * H] for i in range(0, len(vals), W * H)]

    min_layer = min(layers, key=lambda x: x.count(0))
    return min_layer.count(1) * min_layer.count(2)


if EXAMPLE:
    print(solve(input))
else:
    submit(day=8, part=1, answer=solve(input))

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

    image = [2] * W * H
    for layer in layers:
        for i, pixel in enumerate(layer):
            if image[i] == 2:
                image[i] = pixel

    for i in range(0, len(image), W):
        print(''.join(' ' if x == 0 else '#' for x in image[i : i + W]))

    return 'Done'


if EXAMPLE:
    print(solve(input))
else:
    submit(day=8, part=2, answer=solve(input))

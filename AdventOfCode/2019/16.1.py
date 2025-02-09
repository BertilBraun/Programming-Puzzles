from aoc import *
from util import *
from intcode import *


def solve1(input: str) -> str | int | None:
    numbers = np.array([int(x) for x in input])
    base = np.array([0, 1, 0, -1])
    for _ in range(100):
        new_numbers = np.zeros(len(numbers), dtype=int)
        for i in range(len(numbers)):
            pattern = np.tile(np.repeat(base, i + 1), len(numbers) // (4 * (i + 1)) + 1)[1 : len(numbers) + 1]
            new_numbers[i] = abs(np.sum(numbers * pattern)) % 10

        numbers = new_numbers

    return ''.join([str(x) for x in numbers[:8]])


if __name__ == '__main__':
    aoc(day=16, part=1, solve1=solve1, example=False)

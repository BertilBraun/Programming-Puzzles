from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    dial = 50
    count = 0
    for line in input.splitlines():
        value = int(line[1:])
        if line.startswith('L'):
            direction = -1
        elif line.startswith('R'):
            direction = 1
        for _ in range(value):
            dial += direction
            if dial % 100 == 0:
                count += 1
    return count



if __name__ == '__main__':
    aoc(day=1, part=2, solve2=solve2, example=False)

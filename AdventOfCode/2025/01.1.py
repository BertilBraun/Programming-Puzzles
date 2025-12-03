from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    dial = 50
    count = 0
    for line in input.splitlines():
        if line.startswith('L'):
            dial -= int(line[1:])
        elif line.startswith('R'):
            dial += int(line[1:])
        if dial % 100 == 0:
            count += 1
    return count
    


if __name__ == '__main__':
    aoc(day=1, part=1, solve1=solve1, example=False)

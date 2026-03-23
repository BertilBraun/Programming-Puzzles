from aoc import *
from util import *


def hash(s: str) -> int:
    current = 0
    for c in s:
        current = ((current + ord(c)) * 17) % 256
    return current


def solve1(input: str) -> str | int | None:
    return sum(hash(s) for s in input.split(','))


if __name__ == '__main__':
    aoc(day=15, part=1, solve1=solve1, example=False)

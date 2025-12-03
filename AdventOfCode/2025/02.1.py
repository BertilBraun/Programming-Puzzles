from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    ranges = [map(int, range.split('-')) for range in input.split(',')]
    invalid_sum = 0
    for start, end in ranges:
        for v in range(start, end+1):
            s = str(v)
            if len(s) % 2 == 0 and s[:len(s)//2] == s[len(s)//2:]:
                invalid_sum += v
    return invalid_sum


if __name__ == '__main__':
    aoc(day=2, part=1, solve1=solve1, example=False)

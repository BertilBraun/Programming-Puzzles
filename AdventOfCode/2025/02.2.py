from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    ranges = [map(int, range.split('-')) for range in input.split(',')]
    invalid_sum = 0
    for start, end in ranges:
        for v in range(start, end + 1):
            s = str(v)
            for i in range(1, len(s) // 2 + 1):
                repeats_to_complete_s = len(s) // i
                if repeats_to_complete_s * i == len(s) and repeats_to_complete_s * s[:i] == s:
                    invalid_sum += v
                    break
    return invalid_sum


if __name__ == '__main__':
    aoc(day=2, part=2, solve2=solve2, example=False)

from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    freshness, ingredients = input.split('\n\n')
    fresh_ranges = [list(map(int, range.split('-'))) for range in freshness.splitlines()]

    # Transform the ranges into non overlapping ranges
    points = []
    for start, end in fresh_ranges:
        points.append((start, 1))
        points.append((end + 1, -1))
    points.sort()

    new_ranges = []
    current_start = None
    num_open = 0
    for point, type in points:
        if num_open > 0:
            new_ranges.append((current_start, point))
        current_start = point
        num_open += type

    return sum(end - start for start, end in new_ranges)


if __name__ == '__main__':
    aoc(day=5, part=2, solve2=solve2, example=False)

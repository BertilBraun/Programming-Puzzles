from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    points = [Point.parse(line) for line in input.splitlines()]
    largest_area = 0
    for i, p in enumerate(points):
        for q in points[i + 1 :]:
            area = (abs(p.x - q.x) + 1) * (abs(p.y - q.y) + 1)
            largest_area = max(largest_area, area)
    return largest_area


if __name__ == '__main__':
    aoc(day=9, part=1, solve1=solve1, example=False)

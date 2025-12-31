from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    grid = parse_grid(input)

    for i in range(len(grid) - 1, -1, -1):
        if all(v == '.' for v in grid[i]):
            grid.insert(i, list(grid[i]))

    for j in range(len(grid[0]) - 1, -1, -1):
        if all(row[j] == '.' for row in grid):
            for i in range(len(grid)):
                grid[i].insert(j, '.')

    points: list[Point] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '#':
                points.append(Point(j, i))

    return sum(p1.manhattan(p2) for i, p1 in enumerate(points) for p2 in points[i + 1 :])


if __name__ == '__main__':
    aoc(day=11, part=1, solve1=solve1, example=False)

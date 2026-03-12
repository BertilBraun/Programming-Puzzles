from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)

    expanded_rows = []
    expanded_cols = []

    N, M = len(grid), len(grid[0])

    for i in range(N):
        if all(v == '.' for v in grid[i]):
            expanded_rows.append(i)

    for j in range(M):
        if all(row[j] == '.' for row in grid):
            expanded_cols.append(j)

    points: list[Point] = []
    for i in range(N):
        for j in range(M):
            if grid[i][j] == '#':
                points.append(Point(j, i))

    def dist(p1: Point, p2: Point) -> int:
        d = p1.manhattan(p2)
        for i in range(min(p1.y, p2.y), max(p1.y, p2.y)):
            if i in expanded_rows:
                d += 1_000_000 - 1
        for j in range(min(p1.x, p2.x), max(p1.x, p2.x)):
            if j in expanded_cols:
                d += 1_000_000 - 1
        return d

    return sum(dist(p1, p2) for i, p1 in enumerate(points) for p2 in points[i + 1 :])


if __name__ == '__main__':
    aoc(day=11, part=2, solve2=solve2, example=False)

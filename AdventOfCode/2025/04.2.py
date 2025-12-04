from aoc import *
from util import *


def neighbours(x: int, y: int, w: int, h: int) -> list[Point]:
    # return the 8 neighbours of the point (x, y) as long as they are within the bounds of the grid
    return [
        Point(x + dx, y + dy)
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        if 0 <= x + dx < w and 0 <= y + dy < h
    ]


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)
    w, h = len(grid[0]), len(grid)
    total = 0
    changed = True
    while changed:
        changed = False
        for y in range(h):
            for x in range(w):
                if grid[y][x] == '@':
                    if sum(grid[ny][nx] == '@' for nx, ny in neighbours(x, y, w, h)) < 4:
                        grid[y][x] = '.'
                        total += 1
                        changed = True
    return total


if __name__ == '__main__':
    aoc(day=4, part=2, solve2=solve2, example=False)

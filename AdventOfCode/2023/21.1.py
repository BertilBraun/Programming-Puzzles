from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    grid = parse_grid(input)
    start = find_pos(grid, 'S')
    grid[start.y][start.x] = '.'

    N, M = len(grid), len(grid[0])

    current = set([start])
    for _ in range(64):
        next = set()
        for point in current:
            for neighbor in point.cardinal_neighbours():
                if neighbor.in_bounds(N, M) and grid[neighbor.y][neighbor.x] == '.':
                    next.add(neighbor)
        current = next

    return len(current)


if __name__ == '__main__':
    aoc(day=21, part=1, solve1=solve1, example=False)

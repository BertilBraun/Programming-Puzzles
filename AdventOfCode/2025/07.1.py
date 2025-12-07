from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    grid = parse_grid(input)
    S = find_pos(grid, 'S')
    grid[S.y][S.x] = '|'

    N, M = len(grid), len(grid[0])
    for y in range(1, N):
        for x in range(M):
            if grid[y - 1][x] != '|':
                continue
            if grid[y][x] == '.':
                grid[y][x] = '|'
            elif grid[y][x] == '^':
                grid[y][x] = 'A'
                if grid[y][x - 1] != '^':
                    grid[y][x - 1] = '|'
                if grid[y][x + 1] != '^':
                    grid[y][x + 1] = '|'

    return sum(grid[y].count('A') for y in range(N))


if __name__ == '__main__':
    aoc(day=7, part=1, solve1=solve1, example=False)

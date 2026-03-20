from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    grid = parse_grid(input)

    N, M = len(grid), len(grid[0])

    for i in range(N):
        for j in range(M):
            if grid[i][j] == 'O':
                grid[i][j] = '.'
                next_empty_row = i
                while next_empty_row > 0 and grid[next_empty_row - 1][j] == '.':
                    next_empty_row -= 1
                grid[next_empty_row][j] = 'O'

    total = 0
    for row, val in zip(grid, range(N, 0, -1)):
        total += val * row.count('O')

    return total


if __name__ == '__main__':
    aoc(day=14, part=1, solve1=solve1, example=False)

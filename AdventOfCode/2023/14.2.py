from aoc import *
from util import *


@cache
def roll_north(input: str) -> str:
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

    return '\n'.join(''.join(row) for row in grid)


@cache
def roll_south(input: str) -> str:
    grid = parse_grid(input)
    N, M = len(grid), len(grid[0])

    for i in range(N - 1, -1, -1):
        for j in range(M):
            if grid[i][j] == 'O':
                grid[i][j] = '.'
                next_empty_row = i
                while next_empty_row < N - 1 and grid[next_empty_row + 1][j] == '.':
                    next_empty_row += 1
                grid[next_empty_row][j] = 'O'

    return '\n'.join(''.join(row) for row in grid)


@cache
def roll_west(input: str) -> str:
    grid = parse_grid(input)
    N, M = len(grid), len(grid[0])

    for j in range(M):
        for i in range(N):
            if grid[i][j] == 'O':
                grid[i][j] = '.'
                next_empty_col = j
                while next_empty_col > 0 and grid[i][next_empty_col - 1] == '.':
                    next_empty_col -= 1
                grid[i][next_empty_col] = 'O'

    return '\n'.join(''.join(row) for row in grid)


@cache
def roll_east(input: str) -> str:
    grid = parse_grid(input)
    N, M = len(grid), len(grid[0])

    for j in range(M - 1, -1, -1):
        for i in range(N):
            if grid[i][j] == 'O':
                grid[i][j] = '.'
                next_empty_col = j
                while next_empty_col < M - 1 and grid[i][next_empty_col + 1] == '.':
                    next_empty_col += 1
                grid[i][next_empty_col] = 'O'

    return '\n'.join(''.join(row) for row in grid)


def solve2(input: str) -> str | int | None:

    for _ in trange(1_000_000_000):
        input = roll_east(roll_south(roll_west(roll_north(input))))

    grid = parse_grid(input)
    total = 0
    for row, val in zip(grid, range(len(grid), 0, -1)):
        total += val * row.count('O')

    return total


if __name__ == '__main__':
    aoc(day=14, part=2, solve2=solve2, example=False)

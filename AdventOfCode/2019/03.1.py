from aoc import *
from util import *

DAY = 3
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day=3)
else:
    input = get_input(day=3)


def solve(input: str) -> str | int:
    GRID_SIZE = 20000
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    min_dist = 999999999

    for i, values in enumerate(input.split('\n'), start=1):
        moves = [(move[0], int(move[1:])) for move in values.strip().split(',') if move]

        x, y = GRID_SIZE // 2, GRID_SIZE // 2
        for dir, dist in moves:
            for _ in range(dist):
                if dir == 'U':
                    y -= 1
                elif dir == 'D':
                    y += 1
                elif dir == 'L':
                    x -= 1
                elif dir == 'R':
                    x += 1
                else:
                    raise Exception(f'Invalid direction: {dir}')
                if grid[y][x] == 1 and i == 2:
                    min_dist = min(min_dist, abs(x - GRID_SIZE // 2) + abs(y - GRID_SIZE // 2))
                grid[y][x] = i

    return min_dist


if EXAMPLE:
    print(solve(input))
else:
    submit(day=3, part=1, answer=solve(input))

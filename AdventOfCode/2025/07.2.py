from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)
    S = find_pos(grid, 'S')

    H, W = len(grid), len(grid[0])
    counts = [[0] * W for _ in range(H)]
    counts[S.y][S.x] = 1

    for y in range(H - 1):
        for x in range(W):
            val = counts[y][x]
            cell = grid[y][x]
            next_y = y + 1

            # S acts like . (pass through)
            if cell == 'S' or cell == '.':
                counts[next_y][x] += val

            elif cell == '^':
                # Split left
                counts[next_y][x - 1] += val
                # Split right
                counts[next_y][x + 1] += val

    return sum(counts[H - 1])


if __name__ == '__main__':
    aoc(day=7, part=2, solve2=solve2, example=False)

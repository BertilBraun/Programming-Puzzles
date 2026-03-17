from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    def solve_mirror(block: str) -> int:
        grid = parse_grid(block)
        N, M = len(grid), len(grid[0])

        for split_col in range(1, M):
            all_good = True
            for row in range(N):
                for offset in range(1, min(split_col, M - split_col) + 1):
                    if grid[row][split_col + offset - 1] != grid[row][split_col - offset]:
                        all_good = False
            if all_good:
                return split_col

        for split_row in range(1, N):
            all_good = True
            for col in range(M):
                for offset in range(1, min(split_row, N - split_row) + 1):
                    if grid[split_row + offset - 1][col] != grid[split_row - offset][col]:
                        all_good = False
            if all_good:
                return 100 * split_row

        assert False

    return sum(solve_mirror(block) for block in input.split('\n\n'))


if __name__ == '__main__':
    aoc(day=13, part=1, solve1=solve1, example=False)

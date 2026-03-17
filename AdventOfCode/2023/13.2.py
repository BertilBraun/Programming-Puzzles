from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    def solve_mirrors(grid: list[list[str]]) -> list[int]:
        N, M = len(grid), len(grid[0])
        solutions = []

        for split_col in range(1, M):
            all_good = True
            for row in range(N):
                for offset in range(1, min(split_col, M - split_col) + 1):
                    if grid[row][split_col + offset - 1] != grid[row][split_col - offset]:
                        all_good = False
            if all_good:
                solutions.append(split_col)

        for split_row in range(1, N):
            all_good = True
            for col in range(M):
                for offset in range(1, min(split_row, N - split_row) + 1):
                    if grid[split_row + offset - 1][col] != grid[split_row - offset][col]:
                        all_good = False
            if all_good:
                solutions.append(100 * split_row)

        return solutions

    total = 0
    for block in tqdm(input.split('\n\n')):
        grid = parse_grid(block)
        original = set(solve_mirrors(grid))

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = '#' if grid[i][j] == '.' else '.'
                solutions = solve_mirrors(grid)
                grid[i][j] = '#' if grid[i][j] == '.' else '.'

                new_solutions = [solution for solution in solutions if solution not in original]
                if new_solutions:
                    total += new_solutions[0]
                    break

    return total


if __name__ == '__main__':
    aoc(day=13, part=2, solve2=solve2, example=False)

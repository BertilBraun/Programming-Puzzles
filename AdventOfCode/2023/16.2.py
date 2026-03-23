from aoc import *
from util import *


DIR = {'l': (-1, 0), 'r': (1, 0), 'u': (0, -1), 'd': (0, 1)}


def solve2(input: str) -> str | int | None:
    sys.setrecursionlimit(100_000)

    grid = parse_grid(input)
    N, M = len(grid), len(grid[0])

    def solve(startX: int, startY: int, dir: Literal['l', 'r', 'u', 'd']) -> int:

        energized: set[tuple[int, int]] = set()
        seen: set[tuple[int, int, str]] = set()

        def dfs(x: int, y: int, dir: Literal['l', 'r', 'u', 'd']):
            if x < 0 or x >= M or y < 0 or y >= N or (x, y, dir) in seen:
                return

            seen.add((x, y, dir))
            energized.add((x, y))
            cell = grid[y][x]

            if cell == '.':
                dx, dy = DIR[dir]
                dfs(x + dx, y + dy, dir)
            elif cell == '/':
                if dir == 'l':
                    dfs(x, y + 1, 'd')
                elif dir == 'r':
                    dfs(x, y - 1, 'u')
                elif dir == 'u':
                    dfs(x + 1, y, 'r')
                elif dir == 'd':
                    dfs(x - 1, y, 'l')
            elif cell == '\\':
                if dir == 'l':
                    dfs(x, y - 1, 'u')
                elif dir == 'r':
                    dfs(x, y + 1, 'd')
                elif dir == 'u':
                    dfs(x - 1, y, 'l')
                elif dir == 'd':
                    dfs(x + 1, y, 'r')
            elif cell == '|':
                if dir == 'u':
                    dfs(x, y - 1, 'u')
                elif dir == 'd':
                    dfs(x, y + 1, 'd')
                elif dir in 'lr':
                    dfs(x, y - 1, 'u')
                    dfs(x, y + 1, 'd')
            elif cell == '-':
                if dir == 'l':
                    dfs(x - 1, y, 'l')
                elif dir == 'r':
                    dfs(x + 1, y, 'r')
                elif dir in 'ud':
                    dfs(x - 1, y, 'l')
                    dfs(x + 1, y, 'r')

        dfs(startX, startY, dir)

        return len(energized)

    best = 0
    for x in range(M):
        best = max(best, solve(x, 0, 'd'))
        best = max(best, solve(x, N - 1, 'u'))
    for y in range(N):
        best = max(best, solve(0, y, 'r'))
        best = max(best, solve(M - 1, y, 'l'))
    return best


if __name__ == '__main__':
    aoc(day=16, part=2, solve2=solve2, example=False)

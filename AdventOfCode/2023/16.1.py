from aoc import *
from util import *


DIR = {'l': (-1, 0), 'r': (1, 0), 'u': (0, -1), 'd': (0, 1)}


def solve1(input: str) -> str | int | None:
    sys.setrecursionlimit(100_000)

    grid = parse_grid(input)
    N, M = len(grid), len(grid[0])

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

    dfs(0, 0, 'r')

    for y in range(N):
        for x in range(M):
            print('#' if (x, y) in energized else '.', end='')
        print()

    return len(energized)


if __name__ == '__main__':
    aoc(day=16, part=1, solve1=solve1, example=False)

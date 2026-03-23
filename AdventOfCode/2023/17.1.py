from aoc import *
from util import *

DIR = {'l': (-1, 0), 'r': (1, 0), 'u': (0, -1), 'd': (0, 1)}
TURN = {'l': ('u', 'd', 'l'), 'r': ('u', 'd', 'r'), 'u': ('l', 'r', 'u'), 'd': ('l', 'r', 'd')}


def solve1(input: str) -> str | int | None:
    grid = parse_int_grid(input)

    N, M = len(grid), len(grid[0])

    queue = [(0, 0, 0, 'r', 0)]
    visited = set()

    while queue:
        value, x, y, dir, count = heappop(queue)
        if (x, y, dir, count) in visited or x < 0 or x >= M or y < 0 or y >= N:
            continue
        visited.add((x, y, dir, count))

        if x == M - 1 and y == N - 1:
            return value - grid[0][0] + grid[N - 1][M - 1]

        for new_dir in TURN[dir]:
            dx, dy = DIR[new_dir]
            if dir == new_dir and count == 2:
                continue
            new_count = 0 if dir != new_dir else count + 1
            heappush(queue, (value + grid[y][x], x + dx, y + dy, new_dir, new_count))


if __name__ == '__main__':
    aoc(day=17, part=1, solve1=solve1, example=False)

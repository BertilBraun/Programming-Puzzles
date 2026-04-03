from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    plans = []
    for line in input.splitlines():
        dir, dist, color = line.split(' ')
        plans.append((dir, int(dist), color.strip('()')))

    grid = [['.' for _ in range(500)] for _ in range(350)]

    pos = start = Point(250, 250)
    grid[pos.y][pos.x] = '#'

    for dir, dist, _ in plans:
        for _ in range(dist):
            if dir == 'R':
                pos += Point(1, 0)
            elif dir == 'L':
                pos += Point(-1, 0)
            elif dir == 'D':
                pos += Point(0, 1)
            elif dir == 'U':
                pos += Point(0, -1)
            grid[pos.y][pos.x] = '#'

    # And now flood fill since the network is not degenerated

    queue = [start + Point(1, 1)]
    while queue:
        point = queue.pop(0)

        if grid[point.y][point.x] == '.':
            for neighbor in point.cardinal_neighbours():
                queue.append(neighbor)

        grid[point.y][point.x] = '#'

    for row in grid:
        print(''.join(row))

    return sum(row.count('#') for row in grid)


if __name__ == '__main__':
    aoc(day=18, part=1, solve1=solve1, example=False)

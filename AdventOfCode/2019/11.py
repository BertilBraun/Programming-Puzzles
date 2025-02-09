from aoc import *
from util import *
from intcode import *


def solve_part1(input: str) -> str | int | None:
    # Your code for part 1 here
    computer = Computer(input, [])

    pos = Point(0, 0)
    dir = Point(0, -1)
    painted = set()

    colors = defaultdict(int)

    while True:
        color = computer.run(colors[pos])
        if color is None:
            break

        painted.add(pos)
        colors[pos] = color
        dir = dir.rotate90(-1 if computer.run(None) == 0 else 1)
        pos += dir

    return len(painted)


def solve_part2(input: str) -> str | int | None:
    # Your code for part 2 here
    computer = Computer(input, [])

    pos = Point(0, 0)
    dir = Point(0, -1)
    painted = set()

    colors = defaultdict(int)
    colors[pos] = 1

    while True:
        color = computer.run(colors[pos])
        if color is None:
            break

        painted.add(pos)
        colors[pos] = color
        dir = dir.rotate90(-1 if computer.run(None) == 0 else 1)
        pos += dir

    min_pos, max_pos = Point(0, 0), Point(0, 0)
    for p in painted:
        min_pos = Point(min(min_pos.x, p.x), min(min_pos.y, p.y))
        max_pos = Point(max(max_pos.x, p.x), max(max_pos.y, p.y))

    for y in range(min_pos.y, max_pos.y + 1):
        for x in range(min_pos.x, max_pos.x + 1):
            print(' #'[colors[Point(x, y)]], end='')
        print()

    return 'RJLFBUCU'


if __name__ == '__main__':
    aoc(day=11, solve1=solve_part1, solve2=solve_part2, example=False)

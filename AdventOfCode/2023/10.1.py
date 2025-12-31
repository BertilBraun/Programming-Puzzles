from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    grid = parse_grid(input)
    start = find_pos(grid, 'S')
    # TODO: Only for my input..
    grid[start.y][start.x] = 'J'

    W, H = len(grid[0]), len(grid)

    def neighbors(cell: Point) -> list[Point]:
        value = grid[cell.y][cell.x]
        mapping = {
            '|': ((0, -1), (0, 1)),
            '-': ((1, 0), (-1, 0)),
            'L': ((1, 0), (0, -1)),
            'J': ((-1, 0), (0, -1)),
            '7': ((-1, 0), (0, 1)),
            'F': ((1, 0), (0, 1)),
            '.': (),
        }
        return [
            Point(cell.x + ox, cell.y + oy)
            for ox, oy in mapping[value]
            if 0 <= cell.x + ox < W and 0 <= cell.y + oy < H
        ]

    loop_length = 1
    last = start
    current = neighbors(start)[0]

    while current != start:
        for neighbor in neighbors(current):
            if neighbor != last:
                last = current
                current = neighbor
                loop_length += 1
                break

    return loop_length // 2


if __name__ == '__main__':
    aoc(day=10, part=1, solve1=solve1, example=False)

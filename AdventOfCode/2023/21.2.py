from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)
    start = find_pos(grid, 'S')
    grid[start.y][start.x] = '.'

    N, M = len(grid), len(grid[0])

    points_on_curve = []

    current = set([start])
    for t in trange(1, 131 * 3 + 65 + 1):
        next = set()
        for point in current:
            for neighbor in point.cardinal_neighbours():
                if grid[neighbor.y % N][neighbor.x % M] == '.':
                    next.add(neighbor)
        current = next

        if t % 131 == 65:
            print(t, len(current))
            points_on_curve.append((t, len(current)))

    x = np.array([t for t, _ in points_on_curve])
    y = np.array([steps for _, steps in points_on_curve])

    coeffs = np.polyfit(x, y, 2)
    p = np.poly1d(coeffs)
    return int(p(26_501_365))


if __name__ == '__main__':
    aoc(day=21, part=2, solve2=solve2, example=False)

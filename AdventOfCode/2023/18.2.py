from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    dirs = {'0': (1, 0), '1': (0, 1), '2': (-1, 0), '3': (0, -1)}

    x, y = 0, 0
    vertices = [(x, y)]
    boundary = 0

    for line in input.splitlines():
        _, _, color = line.split(' ')
        color = color.strip('()#')
        dist = int(color[:5], 16)
        dx, dy = dirs[color[5]]

        x += dx * dist
        y += dy * dist
        vertices.append((x, y))
        boundary += dist

    # Shoelace formula: compute signed area of polygon from vertices
    area = 0
    for i in range(len(vertices) - 1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]
        area += x1 * y2 - x2 * y1
    area = abs(area) // 2

    # Pick's theorem: total = interior + boundary
    # A = i + b/2 - 1  =>  i + b = A + b/2 + 1
    return area + boundary // 2 + 1


if __name__ == '__main__':
    aoc(day=18, part=2, solve2=solve2, example=False)

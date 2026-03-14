from aoc import *
from util import *


DIRS_BY_TILE = {
    '|': ((0, -1), (0, 1)),
    '-': ((-1, 0), (1, 0)),
    'L': ((0, -1), (1, 0)),
    'J': ((0, -1), (-1, 0)),
    '7': ((0, 1), (-1, 0)),
    'F': ((0, 1), (1, 0)),
    '.': (),
}

EXPANDED_OFFSETS = {
    '|': ((1, 0), (1, 1), (1, 2)),
    '-': ((0, 1), (1, 1), (2, 1)),
    'L': ((1, 0), (1, 1), (2, 1)),
    'J': ((1, 0), (1, 1), (0, 1)),
    '7': ((0, 1), (1, 1), (1, 2)),
    'F': ((2, 1), (1, 1), (1, 2)),
}


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)
    width, height = len(grid[0]), len(grid)
    start = find_pos(grid, 'S')
    # TODO: Only for my input..
    grid[start.y][start.x] = 'J'

    def neighbors(cell: Point) -> list[Point]:
        return [cell + direction for direction in DIRS_BY_TILE[grid[cell.y][cell.x]]]

    # Follow the pipe once to isolate the single main loop.
    loop = {start}
    last = start
    current = neighbors(start)[0]

    while current != start:
        loop.add(current)
        for neighbor in neighbors(current):
            if neighbor != last:
                last = current
                current = neighbor
                break

    expanded_width = width * 3
    expanded_height = height * 3
    expanded = [['.' for _ in range(expanded_width)] for _ in range(expanded_height)]

    # Turn each loop tile into walls on a 3x3 grid so flood fill can pass through gaps correctly.
    for point in loop:
        tile = grid[point.y][point.x]
        for ox, oy in EXPANDED_OFFSETS[tile]:
            expanded[point.y * 3 + oy][point.x * 3 + ox] = '#'

    # Flood fill the outside; any original tile center not reached afterwards is enclosed.
    outside = set()
    queue = deque([Point(0, 0)])
    outside.add(Point(0, 0))

    while queue:
        point = queue.popleft()
        for neighbor in point.cardinal_neighbours():
            if not neighbor.in_bounds(expanded_width, expanded_height):
                continue
            if neighbor in outside:
                continue
            if expanded[neighbor.y][neighbor.x] == '#':
                continue
            outside.add(neighbor)
            queue.append(neighbor)

    inside_count = 0
    for y in range(height):
        for x in range(width):
            point = Point(x, y)
            if point in loop:
                continue
            center = Point(x * 3 + 1, y * 3 + 1)
            if center not in outside:
                inside_count += 1

    return inside_count


if __name__ == '__main__':
    aoc(day=10, part=2, solve2=solve2, example=False)

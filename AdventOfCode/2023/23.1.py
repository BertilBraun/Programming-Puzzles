from aoc import *
from util import *

ARROW_DIR = {'>': Point(1, 0), '<': Point(-1, 0), 'v': Point(0, 1), '^': Point(0, -1)}


def build_graph(grid: list[list[str]]) -> tuple[dict[Point, list[tuple[Point, int]]], Point, Point]:
    rows = len(grid)
    cols = len(grid[0])

    def non_wall_neighbors(point: Point):
        for neigbor in point.cardinal_neighbours():
            if neigbor.in_bounds(cols, rows) and grid[neigbor.y][neigbor.x] != '#':
                yield neigbor

    start = Point(next(x for x in range(cols) if grid[0][x] == '.'), 0)
    end = Point(next(x for x in range(cols) if grid[rows - 1][x] == '.'), rows - 1)

    # Junctions: start, end, and cells with more than 2 non-wall neighbors
    junctions: set[Point] = {start, end}
    for y in range(rows):
        for x in range(cols):
            point = Point(x, y)
            if grid[y][x] != '#' and sum(1 for _ in non_wall_neighbors(point)) > 2:
                junctions.add(point)

    graph: dict[Point, list[tuple[Point, int]]] = {j: [] for j in junctions}

    for junction in junctions:
        for neighbor in non_wall_neighbors(junction):
            # If the junction cell is an arrow, only walk in the arrow's direction
            jcell = grid[junction.y][junction.x]
            if jcell in ARROW_DIR:
                if (neighbor - junction) != ARROW_DIR[jcell]:
                    continue

            # Walk the corridor until we reach another junction
            prev = junction
            curr = neighbor
            dist = 1
            valid = True

            while curr not in junctions:
                cell = grid[curr.y][curr.x]

                if cell in ARROW_DIR:
                    next_ = curr + ARROW_DIR[cell]
                    if next_ == prev:
                        # Arrow points back — this direction is blocked
                        valid = False
                        break
                    prev = curr
                    curr = next_
                else:
                    nexts = [neighbor for neighbor in non_wall_neighbors(curr) if neighbor != prev]
                    if not nexts:
                        valid = False
                        break
                    prev = curr
                    curr = nexts[0]

                dist += 1

            if valid:
                graph[junction].append((curr, dist))

    return graph, start, end


def solve1(input: str) -> str | int | None:
    grid = parse_grid(input)
    graph, start, end = build_graph(grid)

    visited: set[Point] = set()

    def dfs(node: Point) -> int | None:
        if node == end:
            return 0
        visited.add(node)
        best = None
        for neighbor, dist in graph[node]:
            if neighbor not in visited:
                sub = dfs(neighbor)
                if sub is not None:
                    best = max(best, dist + sub) if best is not None else dist + sub
        visited.remove(node)
        return best

    return dfs(start)


if __name__ == '__main__':
    aoc(day=23, part=1, solve1=solve1, example=False)

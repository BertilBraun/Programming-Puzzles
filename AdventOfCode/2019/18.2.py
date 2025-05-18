from aoc import *
from util import *
from intcode import *


def graph_from_grid(grid: list[list[str]]) -> dict[Point, list[Point]]:
    graph: dict[Point, list[Point]] = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '#':
                continue
            point = Point(x, y)
            graph[point] = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_point = Point(x + dx, y + dy)
                if 0 <= new_point.x < len(grid[0]) and 0 <= new_point.y < len(grid):
                    if grid[new_point.y][new_point.x] != '#':
                        graph[point].append(new_point)
    return graph


def reduce_graph(grid: list[list[str]], graph: dict[Point, list[Point]]) -> dict[Point, list[tuple[Point, int]]]:
    # Remove nodes that are not needed
    # For each node, if it has only 2 neighbors, aka a line, remove it
    reduced_graph = {point: [(neighbor, 1) for neighbor in neighbors] for point, neighbors in graph.items()}
    while True:
        for point, neighbors in reduced_graph.items():
            if len(neighbors) == 2 and grid[point.y][point.x] == '.':
                nl, dl = neighbors[0]
                nr, dr = neighbors[1]
                # remove the point from the left neighbor
                reduced_graph[nl] = [el for el in reduced_graph[nl] if el[0] != point]
                # remove the point from the right neighbor
                reduced_graph[nr] = [el for el in reduced_graph[nr] if el[0] != point]
                reduced_graph[nl].append((nr, dl + dr))
                reduced_graph[nr].append((nl, dl + dr))
                del reduced_graph[point]
                break
        else:
            break

    return reduced_graph


def print_graph(graph: dict[Point, list[tuple[Point, int]]]):
    # print the graph to dot format and render it with graphviz
    with open('graph.dot', 'w') as f:
        f.write('graph G {\n')
        for point, neighbors in graph.items():
            for neighbor, dist in neighbors:
                f.write(f'  {point.x}{point.y} -- {neighbor.x}{neighbor.y} [label="{dist}"];\n')
        f.write('}\n')

    os.system('dot -Tpng graph.dot -o graph.png')
    os.system('open graph.png')


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)

    start = Point(0, 0)
    key_locations = {}
    door_locations = {}

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '@':
                start = Point(x, y)
            if grid[y][x].isalpha():
                if grid[y][x].isupper():
                    door_locations[grid[y][x]] = Point(x, y)
                else:
                    key_locations[grid[y][x]] = Point(x, y)

    print(f'Start: {start}')
    print(f'Keys: {key_locations}', len(key_locations))
    print(f'Doors: {door_locations}', len(door_locations))

    grid[start.y][start.x] = '#'
    grid[start.y - 1][start.x] = '#'
    grid[start.y + 1][start.x] = '#'
    grid[start.y][start.x - 1] = '#'
    grid[start.y][start.x + 1] = '#'
    grid[start.y - 1][start.x - 1] = '@'
    grid[start.y - 1][start.x + 1] = '@'
    grid[start.y + 1][start.x - 1] = '@'
    grid[start.y + 1][start.x + 1] = '@'

    graph = graph_from_grid(grid)
    reduced_graph = reduce_graph(grid, graph)
    print_graph(reduced_graph)
    print(len(reduced_graph))

    for x, y in reduced_graph:
        print(f'{x}, {y}: {reduced_graph[Point(x, y)]}')

    # Find the shortest path collect all keys
    # Dykstra

    pq = [
        (
            0,
            # four corners
            (start + Point(-1, -1), start + Point(-1, 1), start + Point(1, -1), start + Point(1, 1)),
            set(),
        )
    ]  # (distance, points, keys)
    visited = set()

    max_key_count = 0

    while pq:
        dist, points, keys = heappop(pq)
        if len(keys) == len(key_locations):
            return dist
        # print('Visiting:', points, keys, 'dist:', dist)
        for i, robot in enumerate(points):
            if (robot, frozenset(keys)) in visited:
                continue
            visited.add((robot, frozenset(keys)))
            for neighbor, weight in reduced_graph[robot]:
                new_keys = keys.copy()
                if grid[neighbor.y][neighbor.x].isalpha():
                    if grid[neighbor.y][neighbor.x].isupper():
                        if grid[neighbor.y][neighbor.x].lower() not in keys:
                            continue
                    else:
                        new_keys.add(grid[neighbor.y][neighbor.x])

                        if len(new_keys) > max_key_count:
                            max_key_count = len(new_keys)
                            print(f'New max key count: {max_key_count} at dist {dist + weight}')

                new_points = list(points)
                new_points[i] = neighbor
                new_points = tuple(new_points)
                heappush(pq, (dist + weight, new_points, new_keys))  # type: ignore


EXAMPLE_INPUT = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""

if __name__ == '__main__':
    aoc(day=18, part=2, solve2=solve2, example=False, example_input=EXAMPLE_INPUT)

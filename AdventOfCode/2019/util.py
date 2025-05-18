from __future__ import annotations
from typing import Iterable
from pprint import pprint  # noqa
from collections import *  # noqa
from itertools import *  # noqa
from heapq import *  # noqa
from math import *  # noqa
import numpy as np
from tqdm import tqdm, trange  # noqa
from functools import *  # noqa
from random import *  # noqa
import re  # noqa
import os  # noqa


def open_day_in_browser(day: int, year: int) -> None:
    os.system(f'explorer https://adventofcode.com/{year}/day/{day}')


def open_file_in_editor(file: str) -> None:
    os.system(f'code {file}')


class Point:
    # a general 2D point class
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: Point | tuple[int, int]) -> Point:
        if isinstance(other, tuple):
            other = Point(*other)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point | tuple[int, int]) -> Point:
        if isinstance(other, tuple):
            other = Point(*other)
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, factor: int) -> Point:
        return Point(self.x * factor, self.y * factor)

    def __neg__(self) -> Point:
        return Point(-self.x, -self.y)

    def __eq__(self, other: Point | tuple[int, int]) -> bool:
        if isinstance(other, tuple):
            other = Point(*other)
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: Point) -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

    def __iter__(self):
        yield self.x
        yield self.y

    def oob(self, N: int, M: int) -> bool:
        return self.x < 0 or self.x >= N or self.y < 0 or self.y >= M

    def in_bounds(self, N: int, M: int) -> bool:
        return not self.oob(N, M)

    def cardinal_neighbours(self) -> list[Point]:
        return [self + Point(*dir) for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]]

    def dist(self, other: Point) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def manhattan(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def angle(self, other: Point) -> float:
        # so that up is 0, right is pi/2, down is pi, left is 3pi/2
        return atan2(other.y - self.y, other.x - self.x) + pi / 2

    def rotate90(self, k: int) -> Point:
        k %= 4
        if k == 0:
            return self
        if k == 1:
            return Point(-self.y, self.x)
        if k == 2:
            return Point(-self.x, -self.y)
        if k == 3:
            return Point(self.y, -self.x)
        assert False, f'Invalid k: {k}'

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y])

    @staticmethod
    def parse(s: str) -> Point:
        first, second = s.split(',')
        # replace all non digits and '-' with empty string
        first = ''.join(c for c in first if c.isdigit() or c == '-')
        second = ''.join(c for c in second if c.isdigit() or c == '-')
        return Point(int(first), int(second))


class Point3:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: Point3 | tuple[int, int, int]) -> Point3:
        if isinstance(other, tuple):
            other = Point3(*other)
        return Point3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Point3 | tuple[int, int, int]) -> Point3:
        if isinstance(other, tuple):
            other = Point3(*other)
        return Point3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __eq__(self, other: Point3 | tuple[int, int, int]) -> bool:
        if isinstance(other, tuple):
            other = Point3(*other)
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other: Point3) -> bool:
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f'Point3({self.x}, {self.y}, {self.z})'

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __getitem__(self, i: int) -> int:
        return [self.x, self.y, self.z][i]

    def copy(self) -> Point3:
        return Point3(self.x, self.y, self.z)

    def oob(self, N: int, M: int, L: int) -> bool:
        return self.x < 0 or self.x >= N or self.y < 0 or self.y >= M or self.z < 0 or self.z >= L

    def in_bounds(self, N: int, M: int, L: int) -> bool:
        return not self.oob(N, M, L)

    def sign(self) -> Point3:
        x_sign = 0 if self.x == 0 else 1 if self.x > 0 else -1
        y_sign = 0 if self.y == 0 else 1 if self.y > 0 else -1
        z_sign = 0 if self.z == 0 else 1 if self.z > 0 else -1
        return Point3(x_sign, y_sign, z_sign)

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    @staticmethod
    def parse(s: str) -> Point3:
        # parse from <x=-8, y=-10, z=0>
        x, y, z = map(int, re.findall(r'-?\d+', s))
        return Point3(x, y, z)


def dijkstra(map: list[list[int]], start: Point, end: Point) -> list[list[int]]:
    N, M = len(map), len(map[0])
    q = [(0, start)]
    distances = [[9999999999] * M for _ in range(N)]
    distances[start.y][start.x] = 0

    while q:
        d, pos = q.pop(0)
        if pos == end:
            break
        for npos in pos.cardinal_neighbours():
            if npos.in_bounds(N, M) and map[npos.y][npos.x] != 1:
                if d + 1 < distances[npos.y][npos.x]:
                    distances[npos.y][npos.x] = d + 1
                    q.append((d + 1, npos))
    return distances


def parse_grid(input: str) -> list[list[str]]:
    return [list(row.strip()) for row in input.split('\n')]


def parse_ints(input: str) -> list[int]:
    return [int(x.strip()) for x in input.split()]


def find_pos(grid: list[list[str]], target: str) -> Point:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == target:
                return Point(x, y)
    raise ValueError(f'{target} not found in grid')


def calculate_overlap(A: Iterable, B: Iterable) -> int:
    equal_count = 0
    for a, b in zip(A, B):
        if a == b:
            equal_count += 1
        else:
            break
    return equal_count


### Graph functions


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

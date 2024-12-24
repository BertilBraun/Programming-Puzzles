from __future__ import annotations
from typing import Iterable
from pprint import pprint  # noqa
from collections import *  # noqa
from itertools import *  # noqa
from heapq import *  # noqa
from math import *  # noqa
from tqdm import tqdm, trange  # noqa
from functools import *  # noqa
from random import *  # noqa


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

    @staticmethod
    def parse(s: str) -> Point:
        first, second = s.split(',')
        # replace all non digits and '-' with empty string
        first = ''.join(c for c in first if c.isdigit() or c == '-')
        second = ''.join(c for c in second if c.isdigit() or c == '-')
        return Point(int(first), int(second))


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

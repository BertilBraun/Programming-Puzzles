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
import re  # noqa
import os  # noqa


def open_day_in_browser(day: int, year: int) -> None:
    os.system(f'explorer https://adventofcode.com/{year}/day/{day}')


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

from __future__ import annotations


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

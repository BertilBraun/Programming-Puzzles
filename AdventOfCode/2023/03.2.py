from aoc import *
from util import *


def all_numbers(grid: list[list[str]]) -> list[tuple[int, int, int, int]]:
    numbers: list[tuple[int, int, int, int]] = []
    for y in range(len(grid)):
        current = ''
        start: int | None = None
        for x in range(len(grid[y])):
            if grid[y][x].isdigit():
                current += grid[y][x]
                if start is None:
                    start = x
            else:
                if current:
                    end = x
                    numbers.append((int(current), y, start, end))  # type: ignore
                current = ''
                start = None
        if current:
            end = len(grid[y])
            numbers.append((int(current), y, start, end))  # type: ignore
    return numbers


def makes_valid(char: str) -> bool:
    return char == '*'


def is_valid(grid: list[list[str]], y: int, x: int) -> tuple[bool, int, int]:
    M, N = len(grid[0]), len(grid)

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < M and 0 <= ny < N:
                if makes_valid(grid[ny][nx]):
                    return True, ny, nx

    return False, 0, 0


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)

    values = defaultdict(lambda: 1)
    visits = defaultdict(int)
    for number, y, start, end in all_numbers(grid):
        for x in range(start, end):
            valid, ny, nx = is_valid(grid, y, x)
            if valid:
                values[(ny, nx)] *= number
                visits[(ny, nx)] += 1
                break

    return sum(values[key] for key in values if visits[key] > 1)


if __name__ == '__main__':
    aoc(day=3, part=2, solve2=solve2, example=False)

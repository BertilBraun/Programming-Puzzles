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
    return char != '.' and not char.isdigit()


def is_valid(grid: list[list[str]], y: int, x: int) -> bool:
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if makes_valid(grid[ny][nx]):
                    return True
    return False


def solve1(input: str) -> str | int | None:
    grid = parse_grid(input)

    total = 0
    for number, y, start, end in all_numbers(grid):
        if any(is_valid(grid, y, x) for x in range(start, end)):
            total += number

    return total


if __name__ == '__main__':
    aoc(day=3, part=1, solve1=solve1, example=False)

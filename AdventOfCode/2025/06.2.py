from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    grid = parse_grid(input)
    column_limits = [0]
    for i in range(len(grid[0])):
        if all(grid[j][i] == ' ' for j in range(len(grid))):
            column_limits.append(i + 1)

    total = 0

    for start, end in zip(column_limits, column_limits[1:] + [len(grid[0])]):
        operation = grid[-1][start]
        column_total = 0 if operation == '+' else 1

        for i in range(start, end):
            string = ''
            for j in range(len(grid) - 1):
                string += grid[j][i]
            if string.strip() == '':
                continue
            value = int(string.replace(' ', ''))
            if operation == '+':
                column_total += value
            elif operation == '*':
                column_total *= value
            else:
                assert False, f'Invalid operation: {operation}'
        total += column_total
    return total

    operations_line = input.splitlines()[-1]
    rows.append(input.splitlines()[-1])
    last_row = input.splitlines()[-1]
    while '  ' in last_row:
        last_row = last_row.replace('  ', ' ')
    rows.append(last_row.split(' '))

    assert all(len(row) == len(rows[0]) for row in rows)

    total = 0
    for i in range(len(rows[0])):
        operation = rows[-1][i]
        column_total = 0 if operation == '+' else 1
        for j in range(len(rows) - 1):
            value = int(rows[j][i])
            if operation == '+':
                column_total += value
            elif operation == '*':
                column_total *= value
            else:
                assert False, f'Invalid operation: {operation}'
        total += column_total
    return total


if __name__ == '__main__':
    aoc(day=6, part=2, solve2=solve2, example=False)

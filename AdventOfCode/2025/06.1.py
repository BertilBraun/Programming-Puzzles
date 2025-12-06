from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    rows = []
    for line in input.splitlines():
        while '  ' in line:
            line = line.replace('  ', ' ')
        rows.append(line.split(' '))

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
    aoc(day=6, part=1, solve1=solve1, example=False)

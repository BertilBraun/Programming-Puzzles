from aoc import *
from util import *
from intcode import *


def solve_part1(input: str) -> str | int | None:
    computer = Computer(input, [1])
    while not computer.done():
        res = computer.run(None)
    return res


def solve_part2(input: str) -> str | int | None:
    computer = Computer(input, [2])
    while not computer.done():
        res = computer.run(None)
    return res


if __name__ == '__main__':
    aoc(day=9, solve1=solve_part1, solve2=solve_part2)

from aoc import *
from util import *
from intcode import *


def solve1(input: str) -> str | int | None:
    computer = Computer(input)

    computer.run_until_input([])

    screen = defaultdict(int)

    for i in range(0, len(computer.outputs), 3):
        x, y, tile = computer.outputs[i : i + 3]
        screen[(x, y)] = tile

    return sum(1 for tile in screen.values() if tile == 2)


if __name__ == '__main__':
    aoc(day=13, part=1, solve1=solve1, example=False)

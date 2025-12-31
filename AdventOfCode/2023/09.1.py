from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    histories = [[int(v) for v in line.split(' ')] for line in input.splitlines()]

    def extrapolate(history: list[int]) -> int:
        if all(v == 0 for v in history):
            return 0
        diff = extrapolate([history[i + 1] - history[i] for i in range(len(history) - 1)])
        return history[-1] + diff

    return sum(extrapolate(history) for history in histories)


if __name__ == '__main__':
    aoc(day=9, part=1, solve1=solve1, example=False)

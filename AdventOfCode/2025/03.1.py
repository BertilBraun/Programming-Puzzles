from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    score = 0
    for bank in input.splitlines():
        max_element = max(bank[:-1])
        max_element_index = bank[:-1].index(max_element)
        max_element_after = max(bank[max_element_index + 1 :])
        score += int(max_element + max_element_after)
    return score


if __name__ == '__main__':
    aoc(day=3, part=1, solve1=solve1, example=False)

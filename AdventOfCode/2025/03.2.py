from aoc import *
from util import *


def max_number(bank: str, digits: int) -> str:
    if digits == 1:
        return max(bank)
    max_element = max(bank[: -(digits - 1)])
    max_element_index = bank[: -(digits - 1)].index(max_element)
    max_element_after = max_number(bank[max_element_index + 1 :], digits - 1)
    return max_element + max_element_after


def solve2(input: str) -> str | int | None:
    score = 0
    for bank in input.splitlines():
        score += int(max_number(bank, 12))
    return score


if __name__ == '__main__':
    aoc(day=3, part=2, solve2=solve2, example=False)

from aoc import *
from util import *


def parse_card(card: str) -> tuple[list[int], list[int]]:
    winning_numbers, my_numbers = card.split(':')[1].split('|')
    return parse_ints(winning_numbers), parse_ints(my_numbers)


def solve1(input: str) -> str | int | None:
    total = 0
    for winning_numbers, my_numbers in [parse_card(x) for x in input.splitlines()]:
        card_total = 1
        for number in my_numbers:
            if number in winning_numbers:
                card_total *= 2
        total += int(card_total / 2)

    return total


if __name__ == '__main__':
    aoc(day=4, part=1, solve1=solve1, example=False)

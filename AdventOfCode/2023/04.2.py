from aoc import *
from util import *


def parse_card(card: str) -> tuple[list[int], list[int]]:
    winning_numbers, my_numbers = card.split(':')[1].split('|')
    return parse_ints(winning_numbers), parse_ints(my_numbers)


def solve2(input: str) -> str | int | None:
    total = 0
    multiplier = defaultdict(lambda: 1)
    for i, (winning_numbers, my_numbers) in enumerate([parse_card(x) for x in input.splitlines()]):
        card_total = 0
        for number in my_numbers:
            if number in winning_numbers:
                card_total += 1

        for j in range(card_total):
            multiplier[i + j + 1] += multiplier[i]

        total += multiplier[i]

    return total


if __name__ == '__main__':
    aoc(day=4, part=2, solve2=solve2, example=False)

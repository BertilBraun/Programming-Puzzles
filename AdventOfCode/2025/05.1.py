from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    freshness, ingredients = input.split('\n\n')
    fresh_ranges = [list(map(int, range.split('-'))) for range in freshness.splitlines()]
    ingredients = set(map(int, ingredients.splitlines()))

    freshness_count = 0
    for ingredient in ingredients:
        for start, end in fresh_ranges:
            if start <= ingredient and ingredient <= end:
                freshness_count += 1
                break

    return freshness_count


if __name__ == '__main__':
    aoc(day=5, part=1, solve1=solve1, example=False)

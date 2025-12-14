from aoc import *
from util import *


def parse(input: str) -> tuple[list[int], defaultdict[str, defaultdict[str, list[tuple[int, int, int]]]]]:
    """seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15"""

    seeds, map = input.split('\n\n', maxsplit=1)
    seeds = parse_ints(seeds.split(':')[1])

    m = defaultdict(lambda: defaultdict(list))

    for map_definition in map.split('\n\n'):
        lines = map_definition.splitlines()
        from_name, to_name = lines[0].split(' ')[0].split('-to-')
        for line in lines[1:]:
            to_value, from_value, length = parse_ints(line)
            m[from_name][to_name].append((to_value, from_value, length))
    return seeds, m


def forward_value(
    current_name: str, next_name: str, value: int, maps: defaultdict[str, defaultdict[str, list[tuple[int, int, int]]]]
) -> int:
    for to_value, from_value, length in maps[current_name][next_name]:
        if value >= from_value and value < from_value + length:
            return to_value + (value - from_value)
    return value


def forward(
    start: str, end: str, value: int, maps: defaultdict[str, defaultdict[str, list[tuple[int, int, int]]]]
) -> int:
    name = start
    while name != end:
        assert len(maps[name]) == 1
        for next_name in maps[name]:
            value = forward_value(name, next_name, value, maps)
            name = next_name
            break
    return value


def solve1(input: str) -> str | int | None:
    seeds, maps = parse(input)

    return min(forward('seed', 'location', value, maps) for value in seeds)


if __name__ == '__main__':
    aoc(day=5, part=1, solve1=solve1, example=False)

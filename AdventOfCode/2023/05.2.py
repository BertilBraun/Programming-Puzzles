from aoc import *
from util import *


def parse(input: str) -> tuple[list[int], list[list[tuple[int, int, int]]]]:
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

    m = []

    for map_definition in map.split('\n\n'):
        current_map = []
        for line in map_definition.splitlines()[1:]:
            to_value, from_value, length = parse_ints(line)
            current_map.append((to_value, from_value, length))
        m.append(current_map)
    return seeds, m


def change_points(map: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    change_points: list[tuple[int, int]] = []
    for to_value, from_value, length in map:
        change_points.append((from_value, to_value - from_value))
        change_points.append((from_value + length, 0))

    change_points.sort(key=lambda x: (x[0], abs(x[1])))

    changed = True
    while changed:
        # if same value is present multiple times, delete the fist occurence
        changed = False
        for i in range(len(change_points) - 1):
            if change_points[i][0] == change_points[i + 1][0]:
                change_points.pop(i)
                changed = True
                break

    change_points.sort()

    print('input map:', map)
    print('change points:', change_points)

    return change_points


def forward_range(value_start: int, value_end: int, change_points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # this function should map a range of values using the map
    # if a subrange is mapped, it should be added to the returned_ranges with the mapped values
    # if a subrange is not mapped, it should be added to the returned_ranges with the original values
    # To do so, we split the range into subranges by sorting the map by start value

    last_offset = 0
    while change_points and change_points[0][0] < value_start:
        last_offset = change_points[0][1]
        change_points.pop(0)
    while change_points and change_points[-1][0] > value_end:
        change_points.pop(-1)

    if not change_points or change_points[0][0] > value_start:
        change_points.insert(0, (value_start, last_offset))
    if not change_points or change_points[-1][0] < value_end:
        change_points.append((value_end, 0))

    subranges = []
    for i in range(len(change_points) - 1):
        value_start, offset_start = change_points[i]
        value_end, offset_end = change_points[i + 1]
        subranges.append((value_start + offset_start, value_end + offset_start))

    print('subranges:', subranges)
    return subranges


def forward(value_start: int, value_end: int, points: list[list[tuple[int, int]]]) -> int:
    print(value_start, value_end)
    current_ranges = [(value_start, value_end)]
    for change_points in points:
        next_ranges = []
        for start, end in current_ranges:
            next_ranges.extend(forward_range(start, end, list(change_points)))
        current_ranges = next_ranges
        print(current_ranges)
    return min(start for start, end in current_ranges)


def solve2(input: str) -> str | int | None:
    seeds, maps = parse(input)

    points = [change_points(map) for map in maps]

    return min(forward(seeds[i], seeds[i] + seeds[i + 1], points) for i in range(0, len(seeds), 2))


if __name__ == '__main__':
    aoc(day=5, part=2, solve2=solve2, example=False)

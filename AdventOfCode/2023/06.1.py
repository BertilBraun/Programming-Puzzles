from aoc import *
from util import *


def remove_double_space(input):
    while '  ' in input:
        input = input.replace('  ', ' ')
    return input


def solve1(input: str) -> str | int | None:
    times, distances = [[int(val) for val in remove_double_space(line).split(' ')[1:]] for line in input.split('\n')]

    total = 1
    for time, distance in zip(times, distances):
        count = 0
        for power_time in range(time):
            my_distance = (time - power_time) * power_time
            if my_distance > distance:
                count += 1
        total *= count
    return total


if __name__ == '__main__':
    aoc(day=6, part=1, solve1=solve1, example=False)

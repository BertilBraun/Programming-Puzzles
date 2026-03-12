from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    time, distance = [int(line.split(':')[1].replace(' ', '')) for line in input.split('\n')]

    count = 0
    for power_time in range(time):
        my_distance = (time - power_time) * power_time
        if my_distance > distance:
            count += 1
    return count


if __name__ == '__main__':
    aoc(day=6, part=2, solve2=solve2, example=False)

from aoc import *
from util import *
from intcode import *


def solve1(input: str) -> str | int | None:
    # Your code for part 1 here
    coords = [Point3.parse(line) for line in input.splitlines()]
    velocities = [Point3(0, 0, 0) for _ in coords]

    for _ in range(1000):
        for i in range(len(coords)):
            for j in range(len(coords)):
                velocities[i] += (coords[j] - coords[i]).sign()
        for i in range(len(coords)):
            coords[i] += velocities[i]

    potential = [sum(abs(c) for c in coord) for coord in coords]
    kinetic = [sum(abs(v) for v in vel) for vel in velocities]

    return sum(p * k for p, k in zip(potential, kinetic))


if __name__ == '__main__':
    aoc(day=12, part=1, solve1=solve1, example=False)

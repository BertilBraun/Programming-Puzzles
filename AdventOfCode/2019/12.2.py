import math
from aoc import *
from util import *
from intcode import *


def solve2(input: str) -> str | int | None:
    # find the period of each axis independently
    periods = [0, 0, 0]

    coords = [Point3.parse(line) for line in input.splitlines()]
    velocities = [Point3(0, 0, 0) for _ in coords]

    initial_coords = [c.copy() for c in coords]

    for step in range(1_000_000_000):
        for i in range(len(coords)):
            for j in range(len(coords)):
                velocities[i] += (coords[j] - coords[i]).sign()

        for i in range(len(coords)):
            coords[i] += velocities[i]

        for axis in range(3):
            if periods[axis] != 0:
                continue
            velocities_match = all(v[axis] == 0 for v in velocities)
            coords_match = all(coords[i][axis] == initial_coords[i][axis] for i in range(len(coords)))
            if velocities_match and coords_match:
                periods[axis] = step + 1

        if all(periods):
            break

    # find the period of the whole system
    return math.lcm(*periods)


if __name__ == '__main__':
    aoc(
        day=12,
        part=2,
        solve2=solve2,
        example=False,
        example_input="""<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""",
    )

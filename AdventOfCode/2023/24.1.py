from aoc import *
from util import *


def calc_intersection(pointA: Point3f, velocityA: Point3f, pointB: Point3f, velocityB: Point3f) -> float | None:
    # Solve pointA + t*velocityA = pointB + s*velocityB (in x/y only)
    # => t*(vA.y*vB.x - vA.x*vB.y) = (pB.y - pA.y)*vB.x - (pB.x - pA.x)*vB.y
    denom = velocityA.y * velocityB.x - velocityA.x * velocityB.y
    if denom == 0:
        return None  # parallel
    numer = (pointB.y - pointA.y) * velocityB.x - (pointB.x - pointA.x) * velocityB.y
    return numer / denom


def solve1(input: str) -> str | int | None:
    stones: list[tuple[Point3f, Point3f]] = []
    for line in input.splitlines():
        point, velocity = line.split('@')
        stones.append((Point3f.parse(point), Point3f.parse(velocity)))

    total = 0
    for i, (pointA, velA) in enumerate(stones):
        for pointB, velB in stones[i + 1 :]:
            t = calc_intersection(pointA, velA, pointB, velB)
            s = calc_intersection(pointB, velB, pointA, velA)
            if t is not None and s is not None and t > 0 and s > 0:
                intersection = pointA + velA * t
                lower = 200000000000000
                upper = 400000000000000
                # lower = 7
                # upper = 27
                if lower <= intersection.x <= upper and lower <= intersection.y <= upper:
                    total += 1
    return total


if __name__ == '__main__':
    aoc(day=24, part=1, solve1=solve1, example=False)

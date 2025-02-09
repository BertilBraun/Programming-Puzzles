from aoc import *
from util import *
from intcode import *


def parse_astroids(input: str) -> list[Point]:
    return [Point(x, y) for y, line in enumerate(parse_grid(input)) for x, c in enumerate(line) if c == '#']


def solve_part1(input: str) -> str | int | None:
    # Your code for part 1 here
    asteroids = parse_astroids(input)

    best = 0
    for a in asteroids:
        angles = set()
        for b in asteroids:
            if a == b:
                continue
            angles.add(a.angle(b))
        if len(angles) > best:
            best = len(angles)
            print(a, best)
    return best


def solve_part2(input: str) -> str | int | None:
    # Your code for part 2 here
    asteroids = parse_astroids(input)

    angle = 0
    station = Point(8, 16)

    asteroids.remove(station)

    removed = [station]

    for _ in range(200):
        angles = defaultdict(list)
        for a in asteroids:
            angles[station.angle(a)].append(a)

        closest = min(angles[angle], key=lambda p: station.dist(p))
        removed.append(closest)
        asteroids.remove(closest)

        all_angles = list(sorted(angles.keys()))
        angle = all_angles[(all_angles.index(angle) + 1) % len(all_angles)]

    last_removed = removed[-1]

    return last_removed.x * 100 + last_removed.y


if __name__ == '__main__':
    aoc(day=10, solve1=solve_part1, solve2=solve_part2, example=False)

from aoc import *
from util import *


def in_between(a: Point3, b: Point3) -> list[Point3]:
    points = []
    for z in range(a.z, b.z + 1):
        for y in range(a.y, b.y + 1):
            for x in range(a.x, b.x + 1):
                points.append(Point3(x, y, z))
    return points


ids = 0


class Brick:
    def __init__(self, start: Point3, end: Point3) -> None:
        assert start.x <= end.x and start.y <= end.y and start.z <= end.z
        assert 0 <= start.x <= 10 and 0 <= start.y <= 10
        self.start = start
        self.end = end
        self.below: list['Brick'] = []
        self.above: list['Brick'] = []
        global ids
        self.id = ids
        ids += 1

    @property
    def on_ground(self):
        return self.lowest == 1

    @property
    def lowest(self):
        return min(self.start.z, self.end.z)

    @property
    def highest(self):
        return max(self.start.z, self.end.z)

    def is_under(self, other: 'Brick'):
        for my_point in in_between(self.start, self.end):
            for other_point in in_between(other.start, other.end):
                if my_point.x == other_point.x and my_point.y == other_point.y and my_point.z < other_point.z:
                    return True
        return False

    def drop_by(self, delta: int):
        self.start -= Point3(0, 0, delta)
        self.end -= Point3(0, 0, delta)

    @property
    def supporting(self):
        return [above for above in self.above if above.lowest - 1 == self.highest]

    @property
    def supported_by(self):
        return [below for below in self.below if below.highest == self.lowest - 1]

    @property
    def disintegrable(self):
        for brick in self.supporting:
            if len(brick.supported_by) == 1:
                return False
        return True


def solve(bricks: list[Brick], i: int):
    q = [bricks[i]]
    fallen = set()

    while q:
        brick = q.pop(0)
        fallen.add(brick.id)

        for other in brick.supporting:
            if all(support.id in fallen for support in other.supported_by):
                q.append(other)

    return len(fallen) - 1


def solve2(input: str) -> str | int | None:
    bricks: list[Brick] = []
    for line in input.splitlines():
        start, end = line.split('~')
        bricks.append(Brick(Point3.parse(start), Point3.parse(end)))

    bricks = list(sorted(bricks, key=lambda x: x.lowest))
    for falling in bricks:
        if falling.on_ground:
            continue

        lower_bricks = [brick for brick in bricks if brick.lowest < falling.lowest]

        highest = 1
        for lower in lower_bricks:
            if lower.is_under(falling):
                highest = max(highest, lower.highest + 1)
                lower.above.append(falling)
                falling.below.append(lower)

        if falling.lowest > highest:
            falling.drop_by(falling.lowest - highest)

    return sum(solve(bricks, i) for i in trange(len(bricks)))


if __name__ == '__main__':
    aoc(day=22, part=2, solve2=solve2, example=False)

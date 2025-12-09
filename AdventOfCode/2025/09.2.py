from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    points = [Point.parse(line) for line in input.splitlines()]

    def does_line_intersect_box(p1: Point, p2: Point, p: Point, q: Point) -> bool:
        if p1.x == p2.x:
            if min(p.x, q.x) + 1 <= p1.x <= max(p.x, q.x) - 1:
                start_y = min(p.y, q.y) + 1
                end_y = max(p.y, q.y) - 1
                if start_y <= p1.y <= end_y:
                    return True
                if start_y <= p2.y <= end_y:
                    return True
                if min(p1.y, p2.y) <= start_y and max(p1.y, p2.y) >= end_y:
                    return True
        elif p1.y == p2.y:
            if min(p.y, q.y) + 1 <= p1.y <= max(p.y, q.y) - 1:
                start_x = min(p.x, q.x) + 1
                end_x = max(p.x, q.x) - 1
                if start_x <= p1.x <= end_x:
                    return True
                if start_x <= p2.x <= end_x:
                    return True
                if min(p1.x, p2.x) <= start_x and max(p1.x, p2.x) >= end_x:
                    return True
        else:
            raise ValueError(f'Invalid line: {p1} {p2}')
        return False

    def does_intersect_any_line(p: Point, q: Point) -> bool:
        for i, p1 in enumerate(points):
            p2 = points[(i + 1) % len(points)]
            # check if the line between p1 and p2 intersects the box between p and q
            if does_line_intersect_box(p1, p2, p, q):
                return True
        return False

    largest_area = 0
    for i, p in enumerate(tqdm(points)):
        for q in points[i + 1 :]:
            area = (abs(p.x - q.x) + 1) * (abs(p.y - q.y) + 1)
            if area > largest_area:
                if not does_intersect_any_line(p, q):
                    largest_area = area
    return largest_area


if __name__ == '__main__':
    aoc(day=9, part=2, solve2=solve2, example=False)

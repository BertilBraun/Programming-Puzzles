from aoc import *
from util import *
from z3 import Int, IntVal, Solver, sat


def solve2(input: str) -> str | int | None:
    stones: list[tuple[Point3, Point3]] = []
    for line in input.splitlines():
        point, velocity = line.split('@')
        stones.append((Point3.parse(point), Point3.parse(velocity)))

    rx, ry, rz = Int('rx'), Int('ry'), Int('rz')
    vrx, vry, vrz = Int('vrx'), Int('vry'), Int('vrz')

    solver = Solver()

    for i, (p, v) in enumerate(stones[:10]):  # Only 10 stones give the unique solution anyways
        t = Int(f't{i}')
        solver.add(t >= 0)
        solver.add(rx + t * vrx == t * IntVal(v.x) + IntVal(p.x))
        solver.add(ry + t * vry == t * IntVal(v.y) + IntVal(p.y))
        solver.add(rz + t * vrz == t * IntVal(v.z) + IntVal(p.z))

    assert solver.check() == sat
    model = solver.model()
    return model.eval(rx).as_long() + model.eval(ry).as_long() + model.eval(rz).as_long()


if __name__ == '__main__':
    aoc(day=24, part=2, solve2=solve2, example=False)

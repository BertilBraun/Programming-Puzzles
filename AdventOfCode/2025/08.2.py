from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    points = [Point3.parse(line) for line in input.splitlines()]
    N = len(points)
    circuit = [i for i in range(N)]
    candidates = [(i, j) for i in range(N) for j in range(i + 1, N)]
    candidates.sort(key=lambda x: points[x[0]].dist(points[x[1]]))

    for i, j in candidates:
        old_circuit_id = circuit[j]
        for k in range(N):
            if circuit[k] == old_circuit_id:
                circuit[k] = circuit[i]
        if all(circuit[k] == circuit[0] for k in range(N)):
            return points[i].x * points[j].x

    assert False, 'No solution found'


if __name__ == '__main__':
    aoc(day=8, part=2, solve2=solve2, example=False)

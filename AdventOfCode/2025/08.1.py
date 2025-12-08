from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    points = [Point3.parse(line) for line in input.splitlines()]
    N = len(points)
    circuit = [i for i in range(N)]
    candidates = [(i, j) for i in range(N) for j in range(i + 1, N)]
    candidates.sort(key=lambda x: points[x[0]].dist(points[x[1]]))

    for i, j in candidates[:1000]:
        old_circuit_id = circuit[j]
        for k in range(N):
            if circuit[k] == old_circuit_id:
                circuit[k] = circuit[i]

    counter = Counter(circuit)
    # 3 max elements of counter
    max_elements = counter.most_common(3)
    print(max_elements)
    return max_elements[0][1] * max_elements[1][1] * max_elements[2][1]


if __name__ == '__main__':
    aoc(day=8, part=1, solve1=solve1, example=False)

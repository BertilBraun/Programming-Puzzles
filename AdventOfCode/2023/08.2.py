import math
from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    instructions, network = input.split('\n\n')

    graph: dict[str, tuple] = {}
    for line in network.splitlines():
        node, destinations = line.split(' = ')
        destinations = destinations.replace('(', '')
        destinations = destinations.replace(')', '')
        L, R = destinations.split(', ')
        graph[node] = (L, R)

    def steps(start) -> int:
        current = start
        for step in range(10**5):
            if current.endswith('Z'):
                # these are always the same loops loops (at least in my input)
                return step
            direction = instructions[step % len(instructions)]
            current = graph[current][direction == 'R']
        assert False

    ends = [steps(start) for start in graph.keys() if start.endswith('A')]
    prod = 1
    for end in ends:
        # find least common multiple by folding on each new step count
        prod = (prod * end) // math.gcd(prod, end)
    return prod


if __name__ == '__main__':
    aoc(day=8, part=2, solve2=solve2, example=False)

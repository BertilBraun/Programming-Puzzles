from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    instructions, network = input.split('\n\n')

    graph = {}
    for line in network.splitlines():
        node, destinations = line.split(' = ')
        destinations = destinations.replace('(', '')
        destinations = destinations.replace(')', '')
        L, R = destinations.split(', ')
        graph[node] = (L, R)

    current = 'AAA'
    for step in range(10**20):
        if current == 'ZZZ':
            return step
        direction = instructions[step % len(instructions)]
        current = graph[current][direction == 'R']


if __name__ == '__main__':
    aoc(day=8, part=1, solve1=solve1, example=False)

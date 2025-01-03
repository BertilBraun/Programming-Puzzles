from aoc import *
from util import *

DAY = 6
EXAMPLE = False  # Change to True to solve the example input

if EXAMPLE:
    input = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
else:
    input = get_input(day=6)


def solve(input: str) -> str | int:
    edges = [line.split(')') for line in input.split('\n')]
    graph = defaultdict(list)
    for s, e in edges:
        graph[s].append(e)

    def dfs(n, d):
        return d + sum(dfs(child, d + 1) for child in graph[n])

    return dfs('COM', 0)


if EXAMPLE:
    print(solve(input))
else:
    submit(day=6, part=1, answer=solve(input))

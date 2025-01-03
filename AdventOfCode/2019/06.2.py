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
K)L
K)YOU
I)SAN"""
else:
    input = get_input(day=6)


def solve(input: str) -> str | int:
    edges = [line.split(')') for line in input.split('\n')]
    graph = defaultdict(list)
    for s, e in edges:
        graph[s].append(e)

    ans = 0

    def dfs(n):
        if n == 'SAN':
            return 0, float('inf')
        if n == 'YOU':
            return float('inf'), 0
        dists = [dfs(child) for child in graph[n]]
        min_dist_to_san = min((d[0] for d in dists), default=float('inf'))
        min_dist_to_you = min((d[1] for d in dists), default=float('inf'))
        if min_dist_to_san != float('inf') and min_dist_to_you != float('inf'):
            nonlocal ans
            print('Meet at', n)
            ans = min_dist_to_san + min_dist_to_you
            return float('inf'), float('inf')
        return min_dist_to_san + 1, min_dist_to_you + 1

    dfs('COM')
    return ans


if EXAMPLE:
    print(solve(input))
else:
    submit(day=6, part=2, answer=solve(input))

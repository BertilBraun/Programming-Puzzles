from aoc import *
from util import *
from collections import defaultdict


def solve1(input: str) -> str | int | None:
    graph = defaultdict(list)
    for line in input.splitlines():
        node, connections = line.split(':')
        connections = connections.split(' ')
        graph[node] = connections

    def dfs(node: str) -> int:
        if node == 'out':
            return 1
        return sum(dfs(connection) for connection in graph[node])

    return dfs('you')


if __name__ == '__main__':
    aoc(day=11, part=1, solve1=solve1, example=False)

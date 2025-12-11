from aoc import *
from util import *
from collections import defaultdict


def solve2(input: str) -> str | int | None:
    graph = defaultdict(list)
    for line in input.splitlines():
        node, connections = line.split(':')
        connections = connections.split(' ')
        graph[node] = connections

    @cache
    def dfs(node: str, has_seen_dac: bool, has_seen_fft: bool) -> int:
        if node == 'out':
            return 1 if has_seen_dac and has_seen_fft else 0
        if node == 'dac':
            has_seen_dac = True
        if node == 'fft':
            has_seen_fft = True
        return sum(dfs(connection, has_seen_dac, has_seen_fft) for connection in graph[node])

    return dfs('svr', False, False)


if __name__ == '__main__':
    aoc(day=11, part=2, solve2=solve2, example=False)

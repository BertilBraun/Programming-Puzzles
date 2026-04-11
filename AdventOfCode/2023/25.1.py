from aoc import *
from util import *
import networkx as nx


def solve1(input: str) -> str | int | None:
    graph: dict[str, list[str]] = defaultdict(list)
    for line in input.splitlines():
        node, connections = line.split(':')
        for connection in connections.strip().split(' '):
            graph[node].append(connection)
            graph[connection].append(node)

    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Find the 3 edges whose removal disconnects the graph
    cut_edges = nx.minimum_edge_cut(G)

    # Remove them
    G.remove_edges_from(cut_edges)

    # The graph now has exactly 2 connected components
    components = list(nx.connected_components(G))

    return len(components[0]) * len(components[1])


if __name__ == '__main__':
    aoc(day=25, part=1, solve1=solve1, example=False)

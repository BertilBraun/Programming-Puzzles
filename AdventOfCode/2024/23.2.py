from util import *

input = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


# undirected edges
edges = [tuple(line.strip().split('-')) for line in input.split('\n')]

graph = defaultdict(set)

for s, e in edges:
    graph[s].add(e)
    graph[e].add(s)


def is_fully_connected(graph, connected_component) -> bool:
    for node in connected_component:
        if not connected_component <= (graph[node] | {node}):
            return False
    return True


largest_connected_component = set()
for n, edges in graph.items():
    for i in range(len(edges)):
        connected_component = (edges - {list(edges)[i]}) | {n}
        if is_fully_connected(graph, connected_component):
            largest_connected_component.add(tuple(sorted(list(connected_component))))

assert len(largest_connected_component) == 1
print(','.join(largest_connected_component.pop()))

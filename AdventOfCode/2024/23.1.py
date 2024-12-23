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

# find 3 connected components
components = set()

for node in graph:
    for neighbor in graph[node]:
        if neighbor == node:
            continue
        for neighbor2 in graph[neighbor]:
            if neighbor2 == node or neighbor2 == neighbor:
                continue
            if neighbor2 in graph[node]:
                components.add(tuple(sorted([node, neighbor, neighbor2])))


print(len([c for c in components if any(n.startswith('t') for n in c)]))

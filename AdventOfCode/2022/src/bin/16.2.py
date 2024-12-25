from util import *


input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def parse_input():
    regex = r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)'
    valves = {}
    for line in input.split('\n'):
        match = re.match(regex, line)
        if match:
            valve = match.group(1)
            flow_rate = int(match.group(2))
            tunnels = match.group(3).split(', ')
            valves[valve] = {
                'flow_rate': flow_rate,
                'tunnels': [(t, 1) for t in tunnels],
            }
    return valves


valves = parse_input()


# print graph using dot
# Write flow values in the nodes, mark them in red if their flow rate is 0
def write_graph():
    with open('graph.dot', 'w') as f:
        f.write('digraph G {\n')
        # undirected edges
        f.write('edge [dir=none]\n')
        for v, data in valves.items():
            f.write(f'{v} [label="{v} {data["flow_rate"]}", color={"red" if data["flow_rate"] == 0 else "black"}]\n')

            # write edges with times
            for tunnel, time in data['tunnels']:
                if tunnel > v:
                    f.write(f'{v} -> {tunnel} [label="{time}"]\n')

        f.write('}')

    os.system('dot -Tpng graph.dot -o graph.png')
    os.system('graph.png')
    exit()


# remove 0 flow rate nodes by removing them from the graph and adding a time to travel to each tunnel
# Only reduce these nodes, where the flow rate == 0 and the degree == 2
# reduce these by removing the connections and adding a tunnel between the two adjacent nodes with a travel time of +1


def reduce_tree():
    reduced = True
    while reduced:
        reduced = False
        for v, data in valves.items():
            if data['flow_rate'] == 0 and len(data['tunnels']) == 2:
                reduced = True
                (n1, time1), (n2, time2) = data['tunnels']
                valves[n1]['tunnels'].remove((v, time1))
                valves[n2]['tunnels'].remove((v, time2))
                valves[n1]['tunnels'].append((n2, time1 + time2))
                valves[n2]['tunnels'].append((n1, time1 + time2))
                del valves[v]
                break

    for i, data in enumerate(valves.values()):
        data['index'] = i


reduce_tree()
# mwrite_graph()

# One min to open a valve, one min to move through a tunnel
# Whats the max released flow after 30mins starting from valve AA


@cache
def max_flow(node: str, time: int, opened: int, num_players: int) -> int:
    if time <= 0:
        if num_players == 0:
            return 0
        return max_flow('AA', 26, opened, num_players - 1)

    fr, id = valves[node]['flow_rate'], valves[node]['index']
    tunnels = valves[node]['tunnels']

    max_flow_if_directly_moved = max(
        max_flow(
            t1,
            time - tt1,
            opened,
            num_players,
        )
        for (t1, tt1) in tunnels
    )

    max_flow_if_opened = 0
    if not (opened & (1 << id)):
        max_flow_if_opened = fr * (time - 1) + max_flow(
            node,
            time - 1,
            opened | (1 << id),
            num_players,
        )

    return max(max_flow_if_opened, max_flow_if_directly_moved)


print(max_flow('AA', 26, 0, 1))

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

regex = r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)'
valves = {}
for line in input.split('\n'):
    match = re.match(regex, line)
    if match:
        valve = match.group(1)
        flow_rate = int(match.group(2))
        tunnels = match.group(3).split(', ')
        valves[valve] = {'flow_rate': flow_rate, 'tunnels': tunnels, 'index': len(valves)}


# One min to open a valve, one min to move through a tunnel
# Whats the max released flow after 30mins starting from valve AA
@cache
def max_flow(valve: str, time: int, opened: tuple[int, ...]) -> int:
    if time <= 0:
        return 0

    assert valve in valves, f'Valve {valve} not found'

    max_flow_if_directly_moved = max(max_flow(tunnel, time - 1, opened) for tunnel in valves[valve]['tunnels'])
    if valves[valve]['flow_rate'] == 0:
        return max_flow_if_directly_moved

    if opened[valves[valve]['index']]:
        return max_flow_if_directly_moved

    new_opened = list(opened)
    new_opened[valves[valve]['index']] = 1
    new_opened = tuple(new_opened)

    max_flow_if_open_then_move = valves[valve]['flow_rate'] * (time - 1) + max(
        max_flow(tunnel, time - 2, new_opened) for tunnel in valves[valve]['tunnels']
    )
    return max(max_flow_if_open_then_move, max_flow_if_directly_moved)


print(max_flow('AA', 30, tuple([0] * len(valves))))

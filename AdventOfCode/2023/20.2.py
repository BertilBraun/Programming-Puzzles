import math
from aoc import *
from util import *
from pathlib import Path

LOW = False
HIGH = True


def solve2(input: str) -> str | int | None:
    graph = {}
    states = {}
    for line in input.splitlines():
        key, destinations = line.split(' -> ')
        type, name = key[0], key[1:]
        destinations = tuple(destinations.split(', '))
        if type == '%':
            states[name] = LOW
        if name == 'roadcaster':
            name = 'broadcaster'
        graph[name] = (type, destinations)

    def incoming(node):
        nodes = []
        for name, (_, destinations) in graph.items():
            if node in destinations:
                nodes.append(name)
        return nodes

    for name, (type, _) in graph.items():
        if type == '&':
            nodes = incoming(name)
            states[name] = (nodes, [LOW] * len(nodes))

    mermaid_lines = ['graph TD']
    for name, (type, destinations) in graph.items():
        if type == '%':
            mermaid_lines.append(f'    {name}["%{name}"]')
        elif type == '&':
            mermaid_lines.append(f'    {name}["&{name}"]')
        else:
            mermaid_lines.append(f'    {name}["{name}"]')
        for dest in destinations:
            mermaid_lines.append(f'    {name} --> {dest}')
    Path(__file__).with_suffix('.mmd').write_text('\n'.join(mermaid_lines) + '\n')

    N = 10000
    first_low = {'ln': N, 'db': N, 'vq': N, 'tf': N}

    for presses in trange(N):
        queue = [('broadcaster', 'button', LOW)]

        while queue:
            node, origin, pulse = queue.pop(0)
            if pulse == LOW and node in first_low:
                first_low[node] = min(presses + 1, first_low[node])
                if all(val < N for val in first_low.values()):
                    return math.lcm(*first_low.values())

            if node not in graph:
                continue
            type, destinations = graph[node]

            if type == '%':
                if pulse == LOW:
                    state = states[node]
                    states[node] = not state
                    for dest in destinations:
                        queue.append((dest, node, not state))
            elif type == '&':
                incoming_nodes, remembered_states = states[node]
                remembered_states[incoming_nodes.index(origin)] = pulse

                next_pulse = LOW if all(remembered_states) else HIGH
                for dest in destinations:
                    queue.append((dest, node, next_pulse))
            elif type == 'b':
                for dest in destinations:
                    queue.append((dest, node, pulse))


if __name__ == '__main__':
    aoc(day=20, part=2, solve2=solve2, example=False)

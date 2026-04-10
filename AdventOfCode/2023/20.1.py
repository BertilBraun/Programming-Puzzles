from aoc import *
from util import *

LOW = False
HIGH = True


def solve1(input: str) -> str | int | None:
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

    high, low = 0, 0
    for _ in range(1000):
        queue = [('broadcaster', 'button', LOW)]

        while queue:
            node, origin, pulse = queue.pop(0)
            if pulse == HIGH:
                high += 1
            else:
                low += 1
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

    return high * low


if __name__ == '__main__':
    aoc(day=20, part=1, solve1=solve1, example=False)

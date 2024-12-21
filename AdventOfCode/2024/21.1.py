from collections import defaultdict
from functools import cache
from util import Point, find_pos, parse_grid


number_pad = parse_grid(
    """789
456
123
#0A"""
)
number_pad_A = find_pos(number_pad, 'A')
number_pad_pos = {char: find_pos(number_pad, char) for char in '1234567890A'}

directional_pad = parse_grid(
    """#^A
<v>"""
)
directional_pad_A = find_pos(directional_pad, 'A')
directional_pad_pos = {char: find_pos(directional_pad, char) for char in '<>^vA'}

input = """029A
980A
179A
456A
379A"""
requested_codes = [line.strip() for line in input.split('\n')]

# Goal: find the input commands over two directional pads that will lead to the requested codes being entered on the number pad
# Output: the minimum number of commands that will lead to the requested code being entered on the number pad
# Commands: A, ^, v, <, >

# Approach:
# The shortest input command sequence will always be one, where each movement has the least amount of direction changes.
# Therefore we should be able to start on the number pad, find the shortest path of the requested code on the number pad by only changing the direction once at most.
# We then should be able to find the shortest path on the directional pad by only changing the direction once at most there as well.

# for 029A: we start on A, move '<' to 0, 'A', then '^' to two, 'A', then '^^>' or '>^^' to 9, 'A' then 'vvv' to A, 'A'


def get_delta(direction: str) -> tuple[int, int]:
    if direction == '^':
        return (0, -1)
    if direction == 'v':
        return (0, 1)
    if direction == '>':
        return (1, 0)
    if direction == '<':
        return (-1, 0)
    assert False, f'Invalid direction {direction}'


def is_path_legal(path: str, pad: list[list[str]], start_pos: Point) -> bool:
    pos = start_pos
    for direction in path:
        move = get_delta(direction)
        pos += move
        if pos.oob(len(pad[0]), len(pad)) or pad[pos.y][pos.x] == '#':
            return False
    return True


def calculate_shortest_pad_paths(
    pad_positions: dict[str, Point], pad: list[list[str]]
) -> dict[tuple[str, str], set[str]]:
    shortest_pad_paths: dict[tuple[str, str], set[str]] = defaultdict(set)

    for start, pos in pad_positions.items():
        for end, end_pos in pad_positions.items():
            dir = end_pos - pos
            xchar = '>' if dir.x > 0 else '<'
            ychar = 'v' if dir.y > 0 else '^'

            xfirst = xchar * abs(dir.x) + ychar * abs(dir.y)
            yfirst = ychar * abs(dir.y) + xchar * abs(dir.x)
            if is_path_legal(xfirst, pad, pos):
                shortest_pad_paths[(start, end)].add(xfirst)
            if is_path_legal(yfirst, pad, pos):
                shortest_pad_paths[(start, end)].add(yfirst)

    return shortest_pad_paths


shortest_number_pad_paths = calculate_shortest_pad_paths(number_pad_pos, number_pad)
shortest_directional_pad_paths = calculate_shortest_pad_paths(directional_pad_pos, directional_pad)


shortest_pad_paths_mp = {
    'number': shortest_number_pad_paths,
    'directional': shortest_directional_pad_paths,
}


@cache
def min_path_length(code: str, num_recursions: int, shortest_pad_paths_id: str) -> int:
    if num_recursions == 0:
        return len(code)

    subpath_min_lengths: list[int] = []
    code = 'A' + code
    for i in range(len(code) - 1):
        paths = shortest_pad_paths_mp[shortest_pad_paths_id][(code[i], code[i + 1])]
        subpath_min_lengths.append(
            min(min_path_length(path + 'A', num_recursions - 1, 'directional') for path in paths)
        )

    return sum(subpath_min_lengths)


print(sum(min_path_length(code, 3, 'number') * int(code[:-1]) for code in requested_codes))

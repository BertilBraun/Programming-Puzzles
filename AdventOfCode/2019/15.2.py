from aoc import *
from util import *
from intcode import *


def solve2(program: str) -> str | int | None:
    computer = Computer(program)

    maze = {}
    pos = Point(0, 0)
    maze[pos] = 1

    def move(pos, direction):
        directions = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]
        return pos + directions[direction]

    def invert(direction):
        if direction == 1:
            return 2
        if direction == 2:
            return 1
        if direction == 3:
            return 4
        if direction == 4:
            return 3
        assert False

    # explore the maze
    def dfs(pos):
        for direction in range(4):
            new_pos = move(pos, direction)
            if new_pos not in maze:
                computer.run_until_input([direction + 1])
                assert len(computer.outputs) == 1
                maze[new_pos] = computer.outputs.pop()
                if maze[new_pos] == 2:
                    print('Found oxygen at', new_pos)
                if maze[new_pos] == 0:
                    continue
                dfs(new_pos)
                computer.run_until_input([invert(direction + 1)])
                assert len(computer.outputs) == 1
                computer.outputs.pop()

    dfs(pos)

    min_x, max_x = min(p.x for p in maze), max(p.x for p in maze)
    min_y, max_y = min(p.y for p in maze), max(p.y for p in maze)

    # print the maze
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) == pos:
                print('X', end='')
            else:
                print('# D'[maze.get(Point(x, y), 0)], end='')
        print()

    # BFS from the oxygen to find the longest path
    oxygen = [pos for pos, value in maze.items() if value == 2][0]
    print('Oxygen at', oxygen)

    pos = oxygen
    queue = [(pos, 0)]
    visited = set()
    max_steps = 0

    while queue:
        pos, steps = queue.pop(0)
        max_steps = max(max_steps, steps)
        for direction in range(4):
            new_pos = move(pos, direction)
            if maze.get(new_pos, 0) == 1 and new_pos not in visited:
                queue.append((new_pos, steps + 1))
                visited.add(new_pos)

    return max_steps


if __name__ == '__main__':
    aoc(day=15, part=2, solve2=solve2, example=False)

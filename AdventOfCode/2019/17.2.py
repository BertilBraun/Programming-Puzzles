from aoc import *
from util import *
from intcode import *


def solve2(input: str) -> str | int | None:
    computer = Computer(input)
    computer.run_until_input([])

    # print all indices of 10 in the output
    WIDTH = computer.outputs.index(10)
    HEIGHT = computer.outputs.count(10) - 1
    print(f'WIDTH: {WIDTH}, HEIGHT: {HEIGHT}')

    grid = np.zeros((HEIGHT, WIDTH), dtype=np.int32)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            grid[i, j] = computer.outputs[i * (WIDTH + 1) + j]  # Skip the 10s

    # print the grid
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(chr(grid[i, j]), end='')
        print()

    # find the intersections
    pos = Point(0, 0)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if grid[i, j] != 35 and grid[i, j] != 46:
                pos = Point(j, i)

    dir = Point(0, -1)

    # while the robot can move in the current direction, move in that direction
    # if it can't, find the next direction - should always be a 90 degree turn
    # add direction and distance to the path
    path = []
    dist = 0

    while True:
        # check if the next position is a wall
        next_pos = pos + dir
        if next_pos.oob(WIDTH, HEIGHT) or grid[next_pos.y, next_pos.x] != 35:
            path.append(str(dist))
            dist = 0
            for new_delta, char in ((dir.rotate90(1), 'R'), (dir.rotate90(-1), 'L')):
                next_pos = pos + new_delta
                if not next_pos.oob(WIDTH, HEIGHT) and grid[next_pos.y, next_pos.x] == 35:
                    # turn right
                    path.append(char)
                    dir = new_delta
                    break
            else:
                # no more moves
                break
        dist += 1
        pos = next_pos

    # FOUND BY HAND BY LOOKING AT THE OUTPUT
    print(path)
    A = 'R,6,L,10,R,8,R,8'
    B = 'R,12,L,8,L,10'
    C = 'R,12,L,10,R,6,L,10'

    PROG = 'A,B,A,C,B,C,A,B,A,C'

    code = '\n'.join([PROG, A, B, C, 'n\n'])

    computer = Computer(input)
    computer[0] = 2
    computer.run_until_input([ord(c) for c in code])

    return computer.outputs[-1]


if __name__ == '__main__':
    aoc(day=17, part=2, solve2=solve2, example=False)

from aoc import *
from util import *
from intcode import *

W, H = 42, 25


def solve2(program: str) -> str | int | None:
    screen = defaultdict(int)

    computer = Computer(program)
    computer[0] = 2
    computer.run_until_input([])

    while True:
        for i in range(0, len(computer.outputs), 3):
            x, y, tile = computer.outputs[i : i + 3]
            screen[(x, y)] = tile

        for y in range(H):
            for x in range(W):
                print(' #*=o'[screen[(x, y)]], end='')
            print()

        print('Score:', screen[(-1, 0)])

        ball_pos = [k for k, v in screen.items() if v == 4][0]
        paddle_pos = [k for k, v in screen.items() if v == 3][0]

        if all(v != 2 for v in screen.values()):
            break

        if ball_pos[0] < paddle_pos[0]:
            command = -1
        elif ball_pos[0] > paddle_pos[0]:
            command = 1
        else:
            command = 0

        computer.run_until_input([command])

    return screen[(-1, 0)]


if __name__ == '__main__':
    aoc(day=13, part=2, solve2=solve2, example=False)

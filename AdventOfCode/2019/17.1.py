from aoc import *
from util import *
from intcode import *


def solve1(input: str) -> str | int | None:
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
            if grid[i, j] == 35:
                print('#', end='')
            elif grid[i, j] == 46:
                print(' ', end='')
            else:
                print(chr(grid[i, j]), end='')
        print()

    # find the intersections
    intersections = []
    for i in range(1, HEIGHT - 1):
        for j in range(1, WIDTH - 1):
            if (
                grid[i, j] == 35
                and grid[i - 1, j] == 35
                and grid[i + 1, j] == 35
                and grid[i, j - 1] == 35
                and grid[i, j + 1] == 35
            ):
                intersections.append((i, j))

    # calculate the sum of the coordinates
    return sum([i * j for i, j in intersections])


if __name__ == '__main__':
    aoc(day=17, part=1, solve1=solve1, example=False)

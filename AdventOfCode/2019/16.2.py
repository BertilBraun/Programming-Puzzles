from aoc import *
from util import *
from intcode import *


BASE_PATTERN = [0, 1, 0, -1]


def solve2(input: str) -> str | int | None:
    offset = int(input[:7])

    numbers = [int(x) for x in input * 10_000][offset:]

    def pattern(index: int) -> np.ndarray:
        # return the pattern for the index-th element
        # the pattern is [0, 1, 0, -1] repeated index times
        # and the first element is skipped
        # e.g. for index 2, the pattern is [1, 0, -1, 0, 1, 0, -1, 0, ...]
        # and the first element is skipped

        base = np.array([0, 1, 0, -1], dtype=np.int32)
        x_times_repeated = np.repeat(base, index)
        tiled_repeatition_of_xs = np.repeat(x_times_repeated, len(numbers) // (4 * index) + 1)
        return tiled_repeatition_of_xs[1 : len(numbers) + 1]

    @cache
    def iterate(index: int, repeat: int) -> int:
        # for the index at the repeat-th iteration, return the value
        if repeat == 0:
            return numbers[index]

        result = 0
        for i in range(index, len(numbers)):
            pat = BASE_PATTERN[(i + 1) // (index + 1) % len(BASE_PATTERN)]
            if pat == 0:
                continue

            result += pat * iterate(i, repeat - 1)

        return abs(result) % 10

    for _ in range(100):
        for i in range(len(numbers) - 2, -1, -1):
            numbers[i] = (numbers[i] + numbers[i + 1]) % 10

    return ''.join([str(x) for x in numbers[:8]])

    return ''.join([str(iterate(i, 100)) for i in trange(offset, offset + 8)])


if __name__ == '__main__':
    aoc(day=16, part=2, solve2=solve2, example=False, example_input='80871224585914546619083218645595')

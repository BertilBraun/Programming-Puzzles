from aoc import *
from util import *


def matchesFullPattern(pattern: str, blocks: list[int]) -> bool:
    return blocks == [len(block) for block in pattern.split('.') if len(block)]


def replace(s: str, i: int, c: str) -> str:
    tmp = list(s)
    tmp[i] = c
    return ''.join(tmp)


def solve1(input: str) -> str | int | None:
    def solve(line: str) -> int:
        pattern, blocks = line.split(' ')
        blocks = [int(block) for block in blocks.split(',')]

        @cache
        def backtrack(current: str) -> int:
            if current.count('?') == 0:
                return matchesFullPattern(current, blocks)

            idx = current.index('?')
            return backtrack(replace(current, idx, '#')) + backtrack(replace(current, idx, '.'))

        return backtrack(pattern)

    return sum(solve(line) for line in tqdm(input.splitlines()))


if __name__ == '__main__':
    aoc(day=12, part=1, solve1=solve1, example=False)

from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    def solve(line: str) -> int:
        pattern, blocks = line.split(' ')
        pattern = '?'.join([pattern] * 5)
        blocks = tuple(int(block) for block in ','.join([blocks] * 5).split(','))

        @cache
        def backtrack(idx: int, blockIdx: int, currentRun: int) -> int:
            if idx == len(pattern):
                if currentRun == 0:
                    return int(blockIdx == len(blocks))
                if blockIdx == len(blocks):
                    return 0
                return int(currentRun == blocks[blockIdx] and blockIdx + 1 == len(blocks))

            total = 0
            c = pattern[idx]

            if c in '#?' and blockIdx < len(blocks) and currentRun < blocks[blockIdx]:
                total += backtrack(idx + 1, blockIdx, currentRun + 1)

            if c in '.?':
                if currentRun == 0:
                    total += backtrack(idx + 1, blockIdx, 0)
                elif blockIdx < len(blocks) and currentRun == blocks[blockIdx]:
                    total += backtrack(idx + 1, blockIdx + 1, 0)

            return total

        return backtrack(0, 0, 0)

    return sum(solve(line) for line in tqdm(input.splitlines()))


if __name__ == '__main__':
    aoc(day=12, part=2, solve2=solve2, example=False)

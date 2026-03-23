from aoc import *
from util import *


def hash(s: str) -> int:
    current = 0
    for c in s:
        current = ((current + ord(c)) * 17) % 256
    return current


def solve2(input: str) -> str | int | None:
    map = defaultdict(list)
    for s in input.split(','):
        if s.endswith('-'):
            label = s[:-1]
            map[hash(label)] = [(key, value) for key, value in map[hash(label)] if key != label]
        else:
            key, value = s.split('=')
            entries = map[hash(key)]
            for i in range(len(entries)):
                if entries[i][0] == key:
                    entries[i] = (key, int(value))
                    break
            else:
                entries.append((key, int(value)))

    total = 0
    for key, entries in map.items():
        for i, (_, value) in enumerate(entries):
            total += (key + 1) * (i + 1) * value
    return total


if __name__ == '__main__':
    aoc(day=15, part=2, solve2=solve2, example=False)

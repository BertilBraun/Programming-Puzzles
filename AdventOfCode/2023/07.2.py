from aoc import *
from util import *


def solve2(input: str) -> str | int | None:
    players = [(line.split(' ')[0], int(line.split(' ')[1])) for line in input.splitlines()]

    def typeOfHand(hand: str) -> int:
        counter = Counter(hand)
        counts = list(sorted(counter.values(), reverse=True))

        c0, c1, j = counts[0], counts[1] if len(counts) > 1 else 0, counter['J']

        if c0 + j >= 5:
            return 5
        elif c0 + j >= 4:
            return 4
        elif (c0 == 3 and c1 == 2) or (c0 == 2 and j >= 1 and c1 == 2):
            return 3
        elif c0 + j == 3:
            return 2
        elif c0 == 2 and c1 + j >= 2:
            return 1
        elif c0 + j == 2:
            return 0
        else:
            return -1

    def compare(hand1: str, hand2: str) -> bool:
        t1 = typeOfHand(hand1)
        t2 = typeOfHand(hand2)
        if t1 > t2:
            return True
        if t1 < t2:
            return False

        order = 'AKQT98765432J'

        for v1, v2 in zip(hand1, hand2):
            o1 = order.index(v1)
            o2 = order.index(v2)
            if o1 == o2:
                continue
            if o1 < o2:
                return True
            else:
                return False
        return False

    winning = [0] * len(players)
    for i, p1 in enumerate(players):
        for p2 in players:
            winning[i] += compare(p1[0], p2[0])

    players_copy = list(players)
    players.sort(key=lambda p: winning[players_copy.index(p)])

    return sum(i * bid for i, (_, bid) in enumerate(players, start=1))


if __name__ == '__main__':
    aoc(day=7, part=2, solve2=solve2, example=False)

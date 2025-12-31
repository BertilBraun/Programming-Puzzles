from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    players = [(line.split(' ')[0], int(line.split(' ')[1])) for line in input.splitlines()]

    def typeOfHand(hand: str) -> int:
        counter = Counter(hand)
        counts = list(sorted(counter.values(), reverse=True))

        if counts[0] == 5:
            return 5
        elif counts[0] == 4:
            return 4
        elif counts[0] == 3 and counts[1] == 2:
            return 3
        elif counts[0] == 3:
            return 2
        elif counts[0] == 2 and counts[1] == 2:
            return 1
        elif counts[0] == 2:
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

        order = 'AKQJT98765432'

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
    aoc(day=7, part=1, solve1=solve1, example=False)

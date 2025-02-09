from aoc import *
from util import *
from intcode import *


def parse_type_quant(s: str) -> tuple[int, str]:
    quant, type = s.split()
    return int(quant), type


def solve2(input: str) -> str | int | None:
    reactions = {}
    for line in input.splitlines():
        inputs, output = line.split(' => ')
        quant, type = parse_type_quant(output)
        reactions[type] = (quant, [parse_type_quant(i) for i in inputs.split(', ')])

    @cache
    def dist(type: str) -> int:
        if type == 'ORE':
            return 0
        return 1 + max(dist(t) for _, t in reactions[type][1])

    def ore_requirement(fuel: int) -> int:
        all_summed_requirements = defaultdict(int)
        all_summed_requirements['FUEL'] = fuel

        while True:
            type = max(all_summed_requirements, key=dist)
            if type == 'ORE':
                break
            produced, inputs = reactions[type]
            times = (all_summed_requirements[type] + produced - 1) // produced
            print(type, all_summed_requirements[type], times)
            for q, t in inputs:
                all_summed_requirements[t] += q * times
            del all_summed_requirements[type]

        return all_summed_requirements['ORE']

    # bin search over the fuel amount
    my_ore = 1_000_000_000_000

    low = 0
    high = my_ore
    while low < high:
        mid = (low + high) // 2
        if ore_requirement(mid) <= my_ore:
            low = mid + 1
        else:
            high = mid

    return low - 1


if __name__ == '__main__':
    aoc(day=14, part=2, solve2=solve2, example=False)

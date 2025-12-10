from aoc import *
from util import *

from dataclasses import dataclass

from z3 import *


@dataclass
class Machine:
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    lights: list[bool]
    buttons: list[list[int]]
    joltage: list[int]

    @staticmethod
    def parse(s: str) -> 'Machine':
        parts = s.split(' ')
        lights = [c == '#' for c in parts[0].strip('[]')]
        buttons = [[int(num) for num in part.strip('()').split(',')] for part in parts[1:-1]]
        joltage = [int(num) for num in parts[-1].strip('{}').split(',')]
        return Machine(lights, buttons, joltage)


def solve2(input: str) -> str | int | None:
    machines = [Machine.parse(line) for line in input.splitlines()]

    def solve(machine: Machine) -> int:
        # z3 solver, each button has a multiplier variable
        multipliers = [Int(f'x{i}') for i in range(len(machine.buttons))]

        solver = Solver()
        solver.add(And(*[multipliers[i] >= 0 for i in range(len(machine.buttons))]))

        for i, joltage in enumerate(machine.joltage):
            buttons_for_index = [j for j, button in enumerate(machine.buttons) if i in button]
            solver.add(joltage == Sum(*[multipliers[j] for j in buttons_for_index]))

        while solver.check() == sat:
            model = solver.model()
            res = sum(model[multipliers[i]].as_long() for i in range(len(machine.buttons)))
            solver.add(Sum(*[multipliers[i] for i in range(len(machine.buttons))]) < res)

        return res

    return sum(solve(machine) for machine in machines)


if __name__ == '__main__':
    aoc(day=10, part=2, solve2=solve2, example=False)

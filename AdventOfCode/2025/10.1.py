from aoc import *
from util import *

from dataclasses import dataclass


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


def solve1(input: str) -> str | int | None:
    machines = [Machine.parse(line) for line in input.splitlines()]

    def solve(machine: Machine) -> int:
        @cache
        def dp(state: tuple[int, ...], i: int) -> int:
            if state == tuple(machine.lights):
                return 0
            if i == len(machine.buttons):
                return int(1e10)
            button = machine.buttons[i]
            # flip all the lights indexed by the button[i]
            new_state = list(state)
            for idx in button:
                new_state[idx] = not new_state[idx]

            return min(dp(tuple(new_state), i + 1) + 1, dp(state, i + 1))

        return dp(tuple(False for _ in range(len(machine.lights))), 0)

    return sum(solve(machine) for machine in machines)


if __name__ == '__main__':
    aoc(day=10, part=1, solve1=solve1, example=False)

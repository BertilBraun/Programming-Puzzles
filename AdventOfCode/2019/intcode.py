def parse_intcode(prog: str) -> list[int]:
    return [int(x) for x in prog.split(',')]


def run_intcode(prog: list[int]) -> list[int]:
    prog = prog.copy()

    i = 0
    while prog[i] != 99:
        if prog[i] == 1:
            prog[prog[i + 3]] = prog[prog[i + 1]] + prog[prog[i + 2]]
        elif prog[i] == 2:
            prog[prog[i + 3]] = prog[prog[i + 1]] * prog[prog[i + 2]]
        else:
            raise Exception(f'Invalid opcode: {prog[i]}')
        i += 4

    return prog

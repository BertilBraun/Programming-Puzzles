def parse_intcode(prog: str) -> list[int]:
    return [int(x) for x in prog.split(',')]


def run_intcode(prog: list[int], inputs: list[int]) -> list[int]:
    def val(i: int, mode: int) -> int:
        return prog[i] if mode else prog[prog[i]]

    outputs = []
    prog = prog.copy()

    i = 0
    while prog[i] != 99:
        op = prog[i] % 100
        modes = prog[i] // 100
        modes, m1 = divmod(modes, 10)
        modes, m2 = divmod(modes, 10)
        modes, m3 = divmod(modes, 10)

        if op == 1:
            prog[prog[i + 3]] = val(i + 1, m1) + val(i + 2, m2)
            i += 4
        elif op == 2:
            prog[prog[i + 3]] = val(i + 1, m1) * val(i + 2, m2)
            i += 4
        elif op == 3:
            prog[prog[i + 1]] = inputs.pop(0)
            i += 2
        elif op == 4:
            outputs.append(val(i + 1, m1))
            i += 2
        elif op == 5:
            i = val(i + 2, m2) if val(i + 1, m1) else i + 3
        elif op == 6:
            i = val(i + 2, m2) if not val(i + 1, m1) else i + 3
        elif op == 7:
            prog[prog[i + 3]] = 1 if val(i + 1, m1) < val(i + 2, m2) else 0
            i += 4
        elif op == 8:
            prog[prog[i + 3]] = 1 if val(i + 1, m1) == val(i + 2, m2) else 0
            i += 4
        else:
            raise ValueError(f'Invalid opcode {op}')

    return outputs

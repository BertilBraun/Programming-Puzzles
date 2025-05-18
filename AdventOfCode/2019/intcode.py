class Computer:
    def __init__(self, prog: str):
        self.prog = [int(x) for x in prog.split(',')]
        self.outputs = []
        self.i = 0
        self.relative_base = 0
        self.mem: dict[int, int] = {}

    def __getitem__(self, i: int) -> int:
        if i < 0:
            raise ValueError('Negative address')
        if i < len(self.prog):
            return self.prog[i]
        return self.mem.get(i, 0)

    def __setitem__(self, i: int, value: int):
        if i < 0:
            raise ValueError('Negative address')
        if i < len(self.prog):
            self.prog[i] = value
        else:
            self.mem[i] = value

    def val(self, offset: int) -> int:
        """Accesses the memory based on the mode of the instruction"""
        modes = self[self.i] // 100
        access_mode = (modes // (10 ** (offset - 1))) % 10
        val = self[self.i + offset]

        result = -1
        if access_mode == 0:
            result = self[val]  # position mode
        elif access_mode == 1:
            result = val  # immediate mode
        elif access_mode == 2:
            result = self[val + self.relative_base]  # relative mode
        else:
            assert False, f'Invalid mode {access_mode}'

        # self.log('Accessing variable at offset:', offset, 'with mode:', access_mode, 'result:', result, 'val:', val)

        return result

    def set_val(self, offset: int, value: int):
        """Sets the memory based on the mode of the instruction"""
        modes = self[self.i] // 100
        access_mode = (modes // (10 ** (offset - 1))) % 10
        val = self[self.i + offset]

        if access_mode == 0:
            self[val] = value  # position mode
        elif access_mode == 2:
            self[val + self.relative_base] = value  # relative mode
        else:
            # immediate mode is invalid for writing
            assert False, f'Invalid mode {access_mode}'

    def done(self) -> bool:
        return self[self.i] == 99

    def run_until_input(self, inputs: list[int]):
        while not self.done():
            op = self[self.i] % 100

            if op == 1:
                self.log('Adding', self.val(1), self.val(2), 'to', self.val(3))
                self.set_val(3, self.val(1) + self.val(2))
                self.i += 4
            elif op == 2:
                self.log('Multiplying', self.val(1), self.val(2), 'to', self.val(3))
                self.set_val(3, self.val(1) * self.val(2))
                self.i += 4
            elif op == 3:
                if inputs:
                    input = inputs.pop(0)
                else:
                    return

                assert input is not None, 'Input required'
                self.log('Input', input, 'to', self.val(1))
                self.set_val(1, input)
                self.i += 2
            elif op == 4:
                self.log('Outputting', self.val(1))
                res = self.val(1)
                self.i += 2
                self.outputs.append(res)
            elif op == 5:
                self.log('Jumping if true', self.val(1), 'to', self.val(2))
                if self.val(1):
                    self.i = self.val(2)
                else:
                    self.i += 3
            elif op == 6:
                self.log('Jumping if false', self.val(1), 'to', self.val(2))
                if not self.val(1):
                    self.i = self.val(2)
                else:
                    self.i += 3
            elif op == 7:
                self.log('Less than', self.val(1), self.val(2), 'to', self.val(3))
                self.set_val(3, 1 if self.val(1) < self.val(2) else 0)
                self.i += 4
            elif op == 8:
                self.log('Equals', self.val(1), self.val(2), 'to', self.val(3))
                self.set_val(3, 1 if self.val(1) == self.val(2) else 0)
                self.i += 4
            elif op == 9:
                self.log('Adjusting relative base by', self.val(1))
                self.relative_base += self.val(1)
                self.i += 2
            else:
                assert False, f'Invalid opcode {op}'

    def log(self, *args):
        return
        print(
            *args,
            '\t\t\ti:',
            self.i,
            'op:',
            self.prog[self.i],
            'params:',
            self.prog[self.i + 1 : self.i + 4],
            'relative_base:',
            self.relative_base,
        )


def print_output_as_ascii(outputs: list[int]):
    """Prints the output as ASCII characters"""
    for i in range(len(outputs)):
        if outputs[i] == 10:
            print()
        else:
            print(chr(outputs[i]), end='')
    print()


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
            print('Adding', val(i + 1, m1), val(i + 2, m2), 'to', prog[i + 3])
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

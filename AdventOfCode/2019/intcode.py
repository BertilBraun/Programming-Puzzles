class Computer:
    def __init__(self, prog: str, inputs: list[int] = []):
        self.prog = [int(x) for x in prog.split(',')]
        self.inputs = inputs
        self.i = 0
        self.relative_base = 0
        self.mem: dict[int, int] = {}

    def __getitem__(self, i: int) -> int:
        if i < 0:
            raise ValueError('Negative address')
        if i < len(self.prog):
            return self.prog[i]
        return self.mem.get(i, 0)

    def __setitem__(self, i: int, val: int):
        if i < 0:
            raise ValueError('Negative address')
        if i < len(self.prog):
            self.prog[i] = val
        else:
            self.mem[i] = val

    def val(self, offset: int) -> int:
        """Accesses the memory based on the mode of the instruction"""
        modes = self[self.i] // 100
        access_mode = (modes // (10 ** (offset - 1))) % 10
        if access_mode == 0:
            return self[self[self.i + offset]]
        elif access_mode == 1:
            return self[self.i + offset]
        elif access_mode == 2:
            return self[self[self.i + offset] + self.relative_base]
        else:
            assert False, f'Invalid mode {access_mode}'

    def done(self) -> bool:
        return self[self.i] == 99

    def run(self, signal: int | None) -> int | None:
        while not self.done():
            op = self[self.i] % 100

            if op == 1:
                self[self[self.i + 3]] = self.val(1) + self.val(2)
                self.i += 4
            elif op == 2:
                self[self[self.i + 3]] = self.val(1) * self.val(2)
                self.i += 4
            elif op == 3:
                if self.inputs:
                    input = self.inputs.pop(0)
                else:
                    input = signal

                assert input is not None, 'Input required'
                self[self[self.i + 1]] = input
                self.i += 2
            elif op == 4:
                res = self.val(1)
                self.i += 2
                return res
            elif op == 5:
                if self.val(1):
                    self.i = self.val(2)
                else:
                    self.i += 3
            elif op == 6:
                if not self.val(1):
                    self.i = self.val(2)
                else:
                    self.i += 3
            elif op == 7:
                self[self[self.i + 3]] = int(self.val(1) < self.val(2))
                self.i += 4
            elif op == 8:
                self[self[self.i + 3]] = int(self.val(1) == self.val(2))
                self.i += 4
            elif op == 9:
                self.relative_base += self.val(1)
                self.i += 2
            else:
                assert False, f'Invalid opcode {op}'

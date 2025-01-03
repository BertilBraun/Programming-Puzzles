class Computer:
    def __init__(self, prog: str, inputs: list[int] = []):
        self.prog = [int(x) for x in prog.split(',')]
        self.inputs = inputs
        self.i = 0

    def val(self, i: int, mode: int) -> int:
        return self.prog[i] if mode else self.prog[self.prog[i]]

    def done(self) -> bool:
        return self.prog[self.i] == 99

    def run(self, signal: int | None) -> int | None:
        while not self.done():
            op = self.prog[self.i] % 100
            modes = self.prog[self.i] // 100
            modes, m1 = divmod(modes, 10)
            modes, m2 = divmod(modes, 10)
            modes, m3 = divmod(modes, 10)

            if op == 1:
                self.prog[self.prog[self.i + 3]] = self.val(self.i + 1, m1) + self.val(self.i + 2, m2)
                self.i += 4
            elif op == 2:
                self.prog[self.prog[self.i + 3]] = self.val(self.i + 1, m1) * self.val(self.i + 2, m2)
                self.i += 4
            elif op == 3:
                if self.inputs:
                    input = self.inputs.pop(0)
                else:
                    input = signal

                assert input is not None, 'Input required'
                self.prog[self.prog[self.i + 1]] = input
                self.i += 2
            elif op == 4:
                res = self.val(self.i + 1, m1)
                self.i += 2
                return res
            elif op == 5:
                self.i = self.val(self.i + 2, m2) if self.val(self.i + 1, m1) else self.i + 3
            elif op == 6:
                self.i = self.val(self.i + 2, m2) if not self.val(self.i + 1, m1) else self.i + 3
            elif op == 7:
                self.prog[self.prog[self.i + 3]] = 1 if self.val(self.i + 1, m1) < self.val(self.i + 2, m2) else 0
                self.i += 4
            elif op == 8:
                self.prog[self.prog[self.i + 3]] = 1 if self.val(self.i + 1, m1) == self.val(self.i + 2, m2) else 0
                self.i += 4
            else:
                assert False, f'Invalid opcode {op}'

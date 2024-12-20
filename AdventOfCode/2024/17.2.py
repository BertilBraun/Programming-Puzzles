import re


input = """Register A: 51064159
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0"""
sample_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

regex = r'Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.*)'
match = re.match(regex, input)
assert match is not None

register_a = int(match.group(1))
register_b = int(match.group(2))
register_c = int(match.group(3))
program = list(map(int, match.group(4).split(',')))


def run(register_a, register_b, register_c, program, log=False):
    instruct_ptr = 0
    out = []

    while instruct_ptr < len(program) - 1:
        instruct, org_value = program[instruct_ptr], program[instruct_ptr + 1]
        instruct_ptr += 2

        if log:
            print(f'instruct = {instruct}, org_value = {org_value}', end=' ')
        if 0 <= org_value <= 3:
            if log:
                print(f'value = {org_value}')
            value = org_value
        elif org_value == 4:
            if log:
                print('value = A')
            value = register_a
        elif org_value == 5:
            if log:
                print('value = B')
            value = register_b
        elif org_value == 6:
            if log:
                print('value = C')
            value = register_c
        else:
            return [-1]

        if instruct == 0:
            if log:
                print('A = A >> value')
            register_a //= 2**value
        elif instruct == 1:
            if log:
                print('B = B ^ org_value')
            register_b = register_b ^ org_value
        elif instruct == 2:
            if log:
                print('B = value % 8')
            register_b = value % 8
        elif instruct == 3:
            if log:
                print('JMP')
            if register_a != 0:
                instruct_ptr = org_value
        elif instruct == 4:
            if log:
                print('B = B ^ C')
            register_b = register_b ^ register_c
        elif instruct == 5:
            if log:
                print('OUT value % 8')
            out.append(value % 8)
        elif instruct == 6:
            if log:
                print('B = A >> value')
            register_b = register_a // 2**value
        elif instruct == 7:
            if log:
                print('C = A >> value')
            register_c = register_a // 2**value
    return out


run(register_a, register_b, register_c, program, log=True)


solves = set()


def dfs(cur: int, num_bits: int, program_index: int):
    for i in range(2 << 3):
        a = (i << num_bits) + cur

        run_res = run(a, register_b, register_c, program)

        if run_res == program:
            solves.add(a)

        equal_count = 0
        for r, p in zip(run_res, program):
            if r == p:
                equal_count += 1
            else:
                break

        if equal_count >= program_index:
            dfs(a, num_bits + 3, program_index + 1)


for i in range(2 << 12):
    if run(i, register_b, register_c, program)[0] == program[0]:
        dfs(i, 12, 1)

print('Solution:', min(solves))

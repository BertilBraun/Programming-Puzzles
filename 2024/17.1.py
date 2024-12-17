import re


input = """Register A: 51064159
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0"""
input = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

regex = r'Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.*)'
match = re.match(regex, input)
assert match is not None

register_a = int(match.group(1))
register_b = int(match.group(2))
register_c = int(match.group(3))
program = list(map(int, match.group(4).split(',')))


def run(register_a, register_b, register_c, program):
    instruct_ptr = 0
    out = []

    while instruct_ptr < len(program) - 1:
        instruct, org_value = program[instruct_ptr], program[instruct_ptr + 1]
        instruct_ptr += 2

        if 0 <= org_value <= 3:
            value = org_value
        elif org_value == 4:
            value = register_a
        elif org_value == 5:
            value = register_b
        elif org_value == 6:
            value = register_c
        else:
            assert False

        if instruct == 0:
            register_a //= 2**value
        elif instruct == 1:
            register_b = register_b ^ org_value
        elif instruct == 2:
            register_b = value % 8
        elif instruct == 3:
            if register_a != 0:
                instruct_ptr = org_value
        elif instruct == 4:
            register_b = register_b ^ register_c
        elif instruct == 5:
            out.append(value % 8)
        elif instruct == 6:
            register_b = register_a // 2**value
        elif instruct == 7:
            register_c = register_a // 2**value
    return out


print(','.join(map(str, run(register_a, register_b, register_c, program))))

from collections import defaultdict
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

    if not log:

        def print(*args, **kwargs):
            pass

    while instruct_ptr < len(program) - 1:
        instruct, org_value = program[instruct_ptr], program[instruct_ptr + 1]
        instruct_ptr += 2

        print(f'instruct = {instruct}, org_value = {org_value}', end=' ')
        if 0 <= org_value <= 3:
            print(f'value = {org_value}')
            value = org_value
        elif org_value == 4:
            print('value = A')
            value = register_a
        elif org_value == 5:
            print('value = B')
            value = register_b
        elif org_value == 6:
            print('value = C')
            value = register_c
        else:
            return [-1]

        if instruct == 0:
            print('A = A >> value')
            register_a //= 2**value
        elif instruct == 1:
            print('B = B ^ org_value')
            register_b = register_b ^ org_value
        elif instruct == 2:
            print('B = value % 8')
            register_b = value % 8
        elif instruct == 3:
            print('JMP')
            if register_a != 0:
                instruct_ptr = org_value
        elif instruct == 4:
            print('B = B ^ C')
            register_b = register_b ^ register_c
        elif instruct == 5:
            print('OUT value % 8')
            out.append(value % 8)
        elif instruct == 6:
            print('B = A >> value')
            register_b = register_a // 2**value
        elif instruct == 7:
            print('C = A >> value')
            register_c = register_a // 2**value
    return out


run(register_a, register_b, register_c, program)

vals = set(program)
mp = {v: [] for v in vals}

for a in range(2**12):
    out = run(a, register_b, register_c, program)[0]
    if out in vals:
        mp[out].append(a)


def to_bin_string(number):
    return bin(number)[2:].zfill(10)


results = defaultdict(set)

max_depth = 0
CHECKS = 1


def solve(number, x, xs, d=1):
    global max_depth, results
    if d > CHECKS:
        print('Returning', d)
        return  # TODO remove
    max_depth = max(max_depth, d)

    # the first 3 bits of number are indifferent
    # the last 7 bits of number have to be equal to the first 7 bits of a value in mp[x]
    # then we can recurse with that new value as number
    # print('Solve', number, x, xs)
    for a in mp[x]:
        # print(
        #     'Number',
        #     number,
        #     number[:7],
        #     'A',
        #     to_bin_string(a),
        #     to_bin_string(a)[3:],
        #     number[:7] == to_bin_string(a)[3:],
        # )
        if number[:7] == to_bin_string(a)[3:]:
            new_number = to_bin_string(a)[:3] + number
            results[d].add(new_number)
            print(
                f'Found {d=} {new_number=} len={len(new_number)} {run(int(new_number, 2), register_b, register_c, program)} solving for {x=} with {xs=}'
            )
            # r = run(int(new_number, 2), register_b, register_c, program)
            # if len(r) < d + 1 or r[d] != x:
            #     print('WHAT', run(int(new_number, 2), register_b, register_c, program), x, new_number)
            #     continue
            if not xs:
                continue
            solve(new_number, xs[0], xs[1:], d + 1)


program_to_solve = program[::-1]

for v in mp[program_to_solve[0]]:
    solve(to_bin_string(v), program_to_solve[1], program_to_solve[2:])

truth = set()
for i in range(2 ** (10 + (CHECKS) * 3)):
    if run(i, register_b, register_c, program)[: CHECKS + 1] == program_to_solve[: CHECKS + 1]:
        truth.add(i)

for i in range(max_depth + 1):
    results[i] = set([int(res, 2) for res in results[i]])

print('Truth:', len(truth))
print(truth)
print('Results:', len(results[CHECKS]))
print(results[CHECKS])
print('MP:', len(mp[program_to_solve[0]]))
print(run(11, register_b, register_c, program))
print(mp[program_to_solve[0]])
print(mp[program_to_solve[1]])
for t in truth:
    if t not in results[CHECKS]:
        print('WHAT?!', t, run(t, register_b, register_c, program))

for res in results[CHECKS]:
    if res not in truth:
        print('WHAT?!', res, run(res, register_b, register_c, program))

print(f'truth={len(truth)}, results={len(results[CHECKS])}, mp={len(mp[CHECKS - 1])}')
print(all(t in results[CHECKS] for t in truth))
print(max_depth)
print(results)


exit()
print(results[max_depth - 1])
for res in results[max_depth - 1]:
    res = res[7:]
    res_len = len(res)
    res = int(res, 2)
    print(res, run(res, register_b, register_c, program))
    for i in range(2**12):
        if run(i << (res_len) + res, register_b, register_c, program) == program_to_solve:
            print('Found', i)


exit()

print('Results:')
for res in results:
    print(res[7:], int(res[7:], 2), run(int(res, 2), register_b, register_c, program))

print(bin(117440))
LOW = [23348132276634]
m = min(int(res[7:], 2) for res in results)
assert m not in LOW
print(m)

"""
MY SOLUTION:

OUT (A_3 ^ 5 ^ 6 ^ (A >> (A_3 ^ 5))) % 8
A = A >> 3

FROM:
B = A % 8
B = B ^ 5
C = A >> B
B = B ^ 6
A = A >> 3
B = B ^ C
OUT B % 8
JMP

SAMPLE SOLUTION:

A = A >> 3
OUT A % 8
JMP
"""

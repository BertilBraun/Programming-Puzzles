from util import *

input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""


operations = {}

for line in input.split('\n\n')[1].split('\n'):
    if line == '':
        continue
    inputs, output = line.split(' -> ')
    input_vars = inputs.split(' ')[0], inputs.split(' ')[2]
    operation = inputs.split(' ')[1]
    operations[output] = (input_vars, operation)

NUM_INPUT_BITS = len(input.split('\n\n')[0].split('\n')) // 2


def simulate(x, y, ops):
    for i in range(NUM_INPUT_BITS):
        ops[f'x{i:02}'] = (x >> i) & 1, 'ASSIGN'
        ops[f'y{i:02}'] = (y >> i) & 1, 'ASSIGN'

    @cache
    def evaluate(var):
        value, operation = ops[var]
        if operation == 'ASSIGN':
            return int(value)
        elif operation == 'AND':
            return evaluate(value[0]) & evaluate(value[1])
        elif operation == 'OR':
            return evaluate(value[0]) | evaluate(value[1])
        elif operation == 'XOR':
            return evaluate(value[0]) ^ evaluate(value[1])
        assert False

    for var in sorted(operations.keys()):
        if var.startswith('z'):
            index = int(var[1:])
            # check if the evaluation of that variable is correct by comparing it to the expected value at that index
            try:
                res = evaluate(var)
            except RecursionError:
                return -1

            if res != ((x + y) >> index) & 1:
                return index

    return NUM_INPUT_BITS + 1


ALL_POSSIBLE_SWAPS = [(k1, k2) for k1 in operations.keys() for k2 in operations.keys() if k1 < k2]
NUM_SIMULATIONS = 20

swaps = []  # found by running the code below


for i in range(4):
    best_swap = None
    best_score = 0

    for k1, k2 in tqdm(ALL_POSSIBLE_SWAPS):
        ops = operations.copy()
        ops[k1], ops[k2] = ops[k2], ops[k1]

        minimum_correct_digits = min(
            simulate(randint(0, 2**NUM_INPUT_BITS - 1), randint(0, 2**NUM_INPUT_BITS - 1), ops)
            for _ in range(NUM_SIMULATIONS)
        )
        if minimum_correct_digits > best_score:
            print('Found better swap', k1, k2, 'with score', minimum_correct_digits)
            best_score = minimum_correct_digits
            best_swap = (k1, k2)

    swaps.append(best_swap)
    operations[best_swap[0]], operations[best_swap[1]] = operations[best_swap[1]], operations[best_swap[0]]  # type: ignore


# for kq, kj in swaps:
#    operations[kq], operations[kj] = operations[kj], operations[kq]

for i in range(NUM_SIMULATIONS):
    print(simulate(randint(0, 2**NUM_INPUT_BITS - 1), randint(0, 2**NUM_INPUT_BITS - 1), operations))

print(swaps)
sorted_keys = []
for k1, k2 in swaps:
    sorted_keys.append(k1)
    sorted_keys.append(k2)
print(','.join(sorted_keys))

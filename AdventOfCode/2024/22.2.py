from util import *

input = """1
10
100
2024"""
nums = parse_ints(input)


MOD = 16777216
ITERATIONS = 2000


def hash(num: int) -> int:
    num ^= num * 64
    num %= MOD
    num ^= num // 32
    num %= MOD
    num ^= num * 2048
    num %= MOD
    return num


deltas = []

for num in nums:
    num_deltas = []
    for _ in range(ITERATIONS):
        new_hash = hash(num)
        delta = (new_hash % 10) - (num % 10)
        num_deltas.append((delta, (new_hash % 10)))
        num = new_hash
    deltas.append(num_deltas)


mp = defaultdict(int)

for delta in deltas:
    seen = set()
    for i in range(3, len(delta)):
        d = (delta[i - 3][0], delta[i - 2][0], delta[i - 1][0], delta[i][0])

        if d not in seen:
            mp[d] += delta[i][1]
            seen.add(d)

print(max(mp.values()))

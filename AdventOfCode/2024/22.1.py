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


for i in range(ITERATIONS):
    nums = [hash(x) for x in nums]

print(sum(nums))

from functools import cache
import re
import sys


input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

games = []

for block in input.split('\n\n'):
    a, b, prize = block.split('\n')
    a_match = re.match(r'Button A: X\+(\d+), Y\+(\d+)', a)
    b_match = re.match(r'Button B: X\+(\d+), Y\+(\d+)', b)
    prize_match = re.match(r'Prize: X=(\d+), Y=(\d+)', prize)
    if a_match and b_match and prize_match:
        a_x, a_y = map(int, a_match.groups())
        b_x, b_y = map(int, b_match.groups())
        prize_x, prize_y = map(int, prize_match.groups())
        games.append((a_x, a_y, b_x, b_y, prize_x, prize_y))

PRICE_A = 3
PRICE_B = 1


@cache
def search(x, y, a_x, a_y, b_x, b_y, prize_x, prize_y):
    if x == prize_x and y == prize_y:
        return 0
    if x > prize_x or y > prize_y:
        return float('inf')
    return min(
        PRICE_A + search(x + a_x, y + a_y, a_x, a_y, b_x, b_y, prize_x, prize_y),
        PRICE_B + search(x + b_x, y + b_y, a_x, a_y, b_x, b_y, prize_x, prize_y),
    )


sys.setrecursionlimit(10000)

tokens = 0
for a_x, a_y, b_x, b_y, prize_x, prize_y in games:
    search_result = search(0, 0, a_x, a_y, b_x, b_y, prize_x, prize_y)
    if search_result < float('inf'):
        tokens += search_result
print(tokens)

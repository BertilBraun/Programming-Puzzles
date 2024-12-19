input = """3   4
4   3
2   5
1   3
3   9
3   3"""

pairs = [tuple(map(int, line.split())) for line in input.split('\n')]
a, b = [a for a, b in pairs], [b for a, b in pairs]

print(sum(a * b.count(a) for a in a))

import re


input = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

regex = r'mul\((\d+),(\d+)\)'
matches = re.findall(regex, input)

print(sum(int(match[0]) * int(match[1]) for match in matches))

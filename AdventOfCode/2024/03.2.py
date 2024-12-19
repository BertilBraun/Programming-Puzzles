import re


input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

# regex either for
regex = r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))"
matches = re.findall(regex, input)

enabled = True
result = 0
for match in matches:
    if match[3]:
        enabled = True
    elif match[4]:
        enabled = False
    else:
        if enabled:
            result += int(match[1]) * int(match[2])

print(result)

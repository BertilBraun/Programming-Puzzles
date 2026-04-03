from aoc import *
from util import *


def solve1(input: str) -> str | int | None:

    def parse_rule(line: str):
        name, rules = line.split('{')
        rules = rules.strip('}')
        parsed_rules = []
        for rule in rules.split(','):
            if ':' in rule:
                test, next_rule_name = rule.split(':')
                if '<' in test:
                    test_key, test_val = test.split('<')

                    def func(x, next=next_rule_name, key=test_key, val=test_val):
                        return next if x[key] < int(val) else None

                    parsed_rules.append((func, rule))
                elif '>' in test:
                    test_key, test_val = test.split('>')

                    def func(x, next=next_rule_name, key=test_key, val=test_val):
                        return next if x[key] > int(val) else None

                    parsed_rules.append((func, rule))
                else:
                    assert False
            else:
                parsed_rules.append((lambda x: rule, rule))
        return name, parsed_rules

    def run(value):

        current = 'in'
        while True:
            for rule, text in rules[current]:
                next = rule(value)
                if next == 'A':
                    print('Accepted', value)
                    return sum(value.values())
                if next == 'R':
                    return 0
                if next is not None:
                    current = next
                    break

    def parse_value(line: str):
        d = {}
        for entry in line.strip('{}').split(','):
            key, value = entry.split('=')
            d[key] = int(value)
        return d

    rules_input, values_input = input.split('\n\n')

    rules = {}
    for line in rules_input.splitlines():
        name, parsed_rules = parse_rule(line)
        rules[name] = parsed_rules

    total = 0

    for value_input in values_input.splitlines():
        value = parse_value(value_input)
        total += run(value)

    return total


if __name__ == '__main__':
    aoc(day=19, part=1, solve1=solve1, example=False)

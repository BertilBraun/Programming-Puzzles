from aoc import *
from util import *


def solve2(input: str) -> str | int | None:

    def parse_rule(line: str):
        name, rules = line.split('{')
        rules = rules.strip('}')
        parsed_rules = []
        for rule in rules.split(','):
            if ':' in rule:
                test, next_rule_name = rule.split(':')
                if '<' in test:
                    test_key, test_val = test.split('<')

                    def func(value, next=next_rule_name, key=test_key, val=test_val):
                        low, high = value[key]
                        new_value = value.copy()
                        new_value[key] = (low, min(high, int(val) - 1))
                        rest_no_match = value.copy()
                        rest_no_match[key] = (max(low, int(val)), high)
                        return next, new_value, rest_no_match

                    parsed_rules.append((func, rule))
                elif '>' in test:
                    test_key, test_val = test.split('>')

                    def func(value, next=next_rule_name, key=test_key, val=test_val):
                        low, high = value[key]
                        new_value = value.copy()
                        new_value[key] = (max(low, int(val) + 1), high)
                        rest_no_match = value.copy()
                        rest_no_match[key] = (low, min(high, int(val)))
                        return next, new_value, rest_no_match

                    parsed_rules.append((func, rule))
                else:
                    assert False
            else:
                parsed_rules.append((lambda x: (rule, x, None), rule))
        return name, parsed_rules

    rules_input, _ = input.split('\n\n')

    rules = {}
    for line in rules_input.splitlines():
        name, parsed_rules = parse_rule(line)
        rules[name] = parsed_rules

    def run(value, current):
        if current == 'A':
            return prod([(high - low + 1) for low, high in value.values()])
        if current == 'R':
            return 0
        if any(high < low for low, high in value.values()):
            return 0

        total = 0
        for rule, text in rules[current]:
            next_name, next_value, rest = rule(value.copy())
            total += run(next_value, next_name)
            value = rest
        return total

    return run({key: [1, 4000] for key in 'xmas'}, 'in')


if __name__ == '__main__':
    aoc(day=19, part=2, solve2=solve2, example=False)

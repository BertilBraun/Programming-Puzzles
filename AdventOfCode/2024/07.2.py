from functools import cache
from tqdm import tqdm


input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

e = [(int(x.split(':')[0]), tuple(map(int, x.split(':')[1].split()))) for x in input.split('\n')]


def oeval(target, values):
    @cache
    def evaluate(i, num):
        if i == len(values):
            return target == num

        if num > target:
            return False

        if evaluate(i + 1, num * values[i]):
            return True
        if evaluate(i + 1, num + values[i]):
            return True
        if evaluate(i + 1, int(str(num) + str(values[i]))):
            return True

        return False

    return evaluate(0, 0)


print(sum(num for num, values in tqdm(e) if oeval(num, values)))

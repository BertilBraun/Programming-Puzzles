from functools import cache


input = '5178527 8525 22 376299 3 69312 0 275'

nums = [int(x) for x in input.split()]


def num_digits(n):
    c = 0
    while n > 0:
        c += 1
        n //= 10
    return c


def split_num(n, c):
    # split n of c digits into two parts
    split = 10 ** (c // 2)
    return divmod(n, split)


@cache
def nums_for_iterations(num, num_iterations):
    if num_iterations == 0:
        return 1

    if num == 0:
        return nums_for_iterations(1, num_iterations - 1)
    elif (c := num_digits(num)) % 2 == 0:
        n1, n2 = split_num(num, c)
        return nums_for_iterations(n1, num_iterations - 1) + nums_for_iterations(n2, num_iterations - 1)
    else:
        return nums_for_iterations(num * 2024, num_iterations - 1)


print(sum(nums_for_iterations(n, 75) for n in nums))

input = '5178527 8525 22 376299 3 69312 0 275'

nums = [int(x) for x in input.split()]

for _ in range(25):
    new_nums = []
    for n in nums:
        n_str = str(n)
        if n == 0:
            new_nums.append(1)
        elif len(n_str) % 2 == 0:
            new_nums.append(int(n_str[: len(n_str) // 2]))
            new_nums.append(int(n_str[len(n_str) // 2 :]))
        else:
            new_nums.append(n * 2024)
    nums = new_nums

print(len(nums))

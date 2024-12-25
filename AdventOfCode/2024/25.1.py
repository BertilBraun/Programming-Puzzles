input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

# keys if last row is #
# locks if first row is #
# parse heights, i.e. count how many # are in each column and for each lock/key parse a list of heights

locks = []
keys = []

for block in input.split('\n\n'):
    block = [line.strip() for line in block.split('\n') if line.strip()]
    heights = [0] * len(block[0])
    for row in block:
        for i, c in enumerate(row):
            if c == '#':
                heights[i] += 1
    if block[0][0] == '#':
        # lock
        locks.append(heights)
    elif block[-1][0] == '#':
        # key
        keys.append(heights)
    else:
        assert False

print(locks)
print(keys)

matching = 0
for lock in locks:
    for key in keys:
        if all((k + l <= 7) for k, l in zip(key, lock)):
            matching += 1

print(matching)

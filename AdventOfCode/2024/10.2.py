input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

map = [[int(x) for x in line.strip()] for line in input.split('\n')]
N, M = len(map), len(map[0])


# Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).


def trailhead_score(x, y, value):
    if x < 0 or x >= N or y < 0 or y >= M:
        return 0
    if map[x][y] != value:
        return 0
    if value == 9:
        return 1

    return sum(trailhead_score(x + dx, y + dy, value + 1) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)])


print(sum(trailhead_score(x, y, 0) for x in range(N) for y in range(M)))

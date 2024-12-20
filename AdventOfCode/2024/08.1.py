from collections import defaultdict


input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

map = [list(x.strip()) for x in input.split('\n')]

N, M = len(map), len(map[0])
antennas = defaultdict(list)

for i in range(N):
    for j in range(M):
        if map[i][j] != '.':
            antennas[map[i][j]].append((i, j))

antinodes = set()

for list in antennas.values():
    for i, a in enumerate(list):
        for b in list[i + 1 :]:
            dir = (b[0] - a[0], b[1] - a[1])
            c = (b[0] + dir[0], b[1] + dir[1])
            d = (a[0] - dir[0], a[1] - dir[1])

            if 0 <= c[0] < N and 0 <= c[1] < M:
                antinodes.add(c)
            if 0 <= d[0] < N and 0 <= d[1] < M:
                antinodes.add(d)

for a in antinodes:
    map[a[0]][a[1]] = 'x'
for row in map:
    print(''.join(row))
print(len(antinodes))

input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
input = [line.strip() for line in input.split('\n') if line.strip()]


# Flood fill on each type. Count how many cells are in each flood fill. Count the number of cells which are not of the same type as the flood fill.

# I for example, should have a fill count of 4 and an outer count of 8 in the above example.

M, N = len(input), len(input[0])
visited = [[False] * N for _ in range(M)]


def flood_fill(i, j, target):
    if i < 0 or i >= M or j < 0 or j >= N or input[i][j] != target:
        return 0, 1
    if visited[i][j]:
        return 0, 0
    visited[i][j] = True
    fill_count = 1
    outer_count = 0
    for x, y in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        fill, outer = flood_fill(i + x, j + y, target)
        fill_count += fill
        outer_count += outer
    return fill_count, outer_count


res = 0
for i in range(M):
    for j in range(N):
        if not visited[i][j]:
            fill_count, outer_count = flood_fill(i, j, input[i][j])
            res += fill_count * outer_count
            print(f'{input[i][j]}: {fill_count} {outer_count}')
print('Result:', res)

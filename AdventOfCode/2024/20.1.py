input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

map = [list(row.strip()) for row in input.split('\n')]
N, M = len(map), len(map[0])

for i in range(N):
    for j in range(M):
        if map[i][j] == 'S':
            start = (i, j)
        elif map[i][j] == 'E':
            end = (i, j)

R = 2
CHEAT = 50


def dykstra(start: tuple[int, int], end: tuple[int, int]) -> list[list[int]]:
    # make a dykstra search for end, returning the min distance
    # from start to end
    q = [(0, start[0], start[1])]
    distance = [[9999999999] * M for _ in range(N)]
    distance[start[0]][start[1]] = 0

    while q:
        d, i, j = q.pop(0)
        if (i, j) == end:
            return distance
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < M and map[ni][nj] != '#':
                if d + 1 < distance[ni][nj]:
                    distance[ni][nj] = d + 1
                    q.append((d + 1, ni, nj))
    return distance


distances_from_start = dykstra(start, end)
distances_from_end = dykstra(end, start)


def cheat_distance(fi: int, fj: int, i: int, j: int) -> int:
    return distances_from_start[fi][fj] + distances_from_end[i][j]


base_distance = cheat_distance(start[0], start[1], start[0], start[1])

cheat_distances = []

for i in range(N):
    for j in range(M):
        for di in range(-R, R + 1):
            for dj in range(-R, R + 1):
                ni, nj = i + di, j + dj
                if ni < 0 or ni >= N or nj < 0 or nj >= M:
                    continue
                cheat_time = abs(di) + abs(dj)
                if cheat_time > R:
                    continue

                dist = base_distance - (cheat_distance(i, j, ni, nj) + cheat_time)
                if dist > 0:
                    cheat_distances.append(dist)


print(len([cheat for cheat in cheat_distances if cheat >= CHEAT]))

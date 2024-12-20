from heapq import heappop, heappush


input = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

maze = [list(row.strip()) for row in input.split('\n')]
N, M = len(maze), len(maze[0])

for x in range(N):
    for y in range(M):
        if maze[x][y] == 'S':
            start = (x, y)
        if maze[x][y] == 'E':
            end = (x, y)

# The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

q = []
heappush(q, (0, start, 0))
visited = set()

while q:
    cost, (x, y), dir = heappop(q)
    if (x, y, dir) in visited:
        continue
    visited.add((x, y, dir))
    if (x, y) == end:
        print(cost)
        break
    nx, ny = x + DIRS[dir][0], y + DIRS[dir][1]
    if 0 <= nx < N and 0 <= ny < M and maze[nx][ny] != '#':
        heappush(q, (cost + 1, (nx, ny), dir))
    for i in [-1, 1]:
        ndir = (dir + i) % 4
        heappush(q, (cost + 1000, (x, y), ndir))

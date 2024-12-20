from util import Point

from heapq import heappop, heappush


input = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

maze = [list(row.strip()) for row in input.split('\n')]
N, M = len(maze), len(maze[0])

for x in range(N):
    for y in range(M):
        if maze[x][y] == 'S':
            start = Point(x, y)
        if maze[x][y] == 'E':
            end = Point(x, y)

# The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


q: list[tuple[int, Point, int, list[Point]]] = []
heappush(q, (0, start, 0, [start]))

end_cost = 9999999999999
all_nodes_visited_on_shortest_path = set()

costs = [[[9999999999999 for _ in range(4)] for _ in range(M)] for _ in range(N)]
costs[start.x][start.y][0] = 0

while q:
    cost, pos, dir, path = heappop(q)
    if pos == end:
        end_cost = cost
        all_nodes_visited_on_shortest_path.update(path)
        continue
    if cost > end_cost:
        break
    if cost > costs[pos.x][pos.y][dir]:
        continue
    costs[pos.x][pos.y][dir] = cost

    new_pos = pos + DIRS[dir]
    if new_pos.in_bounds(N, M) and maze[new_pos.x][new_pos.y] != '#' and cost + 1 < costs[new_pos.x][new_pos.y][dir]:
        heappush(q, (cost + 1, new_pos, dir, path + [new_pos]))

    for i in [-1, 1]:
        ndir = (dir + i + 4) % 4
        if cost + 1000 < costs[pos.x][pos.y][ndir]:
            heappush(q, (cost + 1000, pos, ndir, path))

print(len(all_nodes_visited_on_shortest_path))

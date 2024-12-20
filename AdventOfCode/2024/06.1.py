input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


maze = [list(row.strip()) for row in input.split('\n')]

N, M = len(maze), len(maze[0])

guard = (0, 0)
for i in range(N):
    for j in range(M):
        if maze[i][j] == '^':
            guard = (i, j)

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

current_dir = 0
visited = set()

while True:
    visited.add(guard)
    next_guard = (guard[0] + dirs[current_dir][0], guard[1] + dirs[current_dir][1])
    if next_guard[0] < 0 or next_guard[0] >= N or next_guard[1] < 0 or next_guard[1] >= M:
        break
    if maze[next_guard[0]][next_guard[1]] == '#':
        current_dir = (current_dir + 1) % 4
    else:
        guard = next_guard

for r, c in visited:
    maze[r][c] = 'O'

for row in maze:
    print(''.join(row))

print(len(visited))

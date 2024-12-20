from tqdm import tqdm
from util import Point, dijkstra


input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

points = [Point.parse(line) for line in input.split('\n')]

W = H = 71
W = H = 7

start = Point(0, 0)
end = Point(W - 1, H - 1)

maze = [[0] * W for _ in range(H)]

for p in tqdm(points):
    maze[p.y][p.x] = 1

    # min steps from start to end
    distances = dijkstra(maze, start, end)

    if distances[end.y][end.x] > 99999:
        print('Answer:')
        print(f'{p.x},{p.y}')
        break

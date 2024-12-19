input = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
input = [line.strip() for line in input.split('\n') if line.strip()]


# Flood fill on each type. Count how many cells are in each flood fill. Count the number of cells which are not of the same type as the flood fill.

# I for example, should have a fill count of 4 and an outer count of 8 in the above example.

# outer count should now be the number of straight edges around the area


M, N = len(input), len(input[0])
visited = [[False] * N for _ in range(M)]
current_color = [[0] * (N + 2) for _ in range(M + 2)]


def flood_fill(i, j, target):
    if i < 0 or i >= M or j < 0 or j >= N or input[i][j] != target:
        return 0
    if visited[i][j]:
        return 0
    visited[i][j] = True
    for x, y, v in ((0, 1, 8), (1, 0, 16), (0, -1, 32), (-1, 0, 64)):
        nx, ny = i + x, j + y
        if (
            nx >= -1
            and nx < M + 1
            and ny >= -1
            and ny < N + 1
            and (nx < 0 or nx >= M or ny < 0 or ny >= N or input[nx][ny] != target)
        ):
            current_color[nx][ny] += v
    return 1 + sum(flood_fill(i + x, j + y, target) for x, y in ((0, 1), (0, -1), (1, 0), (-1, 0)))


res = 0
for i in range(M):
    for j in range(N):
        if not visited[i][j]:
            current_color = [[0] * (N + 2) for _ in range(M + 2)]
            fill_count = flood_fill(i, j, input[i][j])
            import numpy as np

            print(np.array(current_color))
            outer_count = 0
            for x in range(M + 2):
                for y in range(N + 2):
                    for dx, dy, v in ((0, 1, 8), (1, 0, 16), (0, -1, 32), (-1, 0, 64)):
                        if current_color[x][y] & v:
                            outer_count += 1
                            current_color[x][y] -= v

                            for left in range(1, 1000):
                                nx, ny = x - dy * left, y + dx * left
                                if nx < 0 or nx >= M + 2 or ny < 0 or ny >= N + 2 or not current_color[nx][ny] & v:
                                    break
                                current_color[nx][ny] -= v

                            for right in range(1, 1000):
                                nx, ny = x + dy * right, y - dx * right
                                if nx < 0 or nx >= M + 2 or ny < 0 or ny >= N + 2 or not current_color[nx][ny] & v:
                                    break

                                current_color[nx][ny] -= v

            res += fill_count * outer_count
            print(f'{input[i][j]}: {fill_count} {outer_count}')
print('Result:', res)

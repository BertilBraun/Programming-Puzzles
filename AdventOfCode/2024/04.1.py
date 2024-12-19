input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

grid = [line.strip() for line in input.split('\n')]

search = 'XMAS'
N, M = len(grid), len(grid[0])

count = 0
# This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words.

for i in range(N):
    for j in range(M):
        if grid[i][j] == search[0]:
            for dx in range(len(search)):
                if j + dx >= M or grid[i][j + dx] != search[dx]:
                    break
            else:
                count += 1

            for dx in range(len(search)):
                if j - dx < 0 or grid[i][j - dx] != search[dx]:
                    break
            else:
                count += 1

            for dy in range(len(search)):
                if i + dy >= N or grid[i + dy][j] != search[dy]:
                    break
            else:
                count += 1

            for dy in range(len(search)):
                if i - dy < 0 or grid[i - dy][j] != search[dy]:
                    break
            else:
                count += 1

            for d in range(len(search)):
                if i + d >= N or j + d >= M or grid[i + d][j + d] != search[d]:
                    break
            else:
                count += 1

            for d in range(len(search)):
                if i - d < 0 or j - d < 0 or grid[i - d][j - d] != search[d]:
                    break
            else:
                count += 1

            for d in range(len(search)):
                if i + d >= N or j - d < 0 or grid[i + d][j - d] != search[d]:
                    break
            else:
                count += 1

            for d in range(len(search)):
                if i - d < 0 or j + d >= M or grid[i - d][j + d] != search[d]:
                    break
            else:
                count += 1


print(count)

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

search = 'MAS'
N, M = len(grid), len(grid[0])

count = 0
# you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

# M.S
# .A.
# M.S

for i in range(1, N - 1):
    for j in range(1, M - 1):
        if grid[i][j] == 'A':
            tl, tr, bl, br = grid[i - 1][j - 1], grid[i - 1][j + 1], grid[i + 1][j - 1], grid[i + 1][j + 1]

            if tl == tr == 'M' and bl == br == 'S':
                count += 1

            if tl == bl == 'M' and tr == br == 'S':
                count += 1

            if tr == br == 'M' and tl == bl == 'S':
                count += 1

            if bl == br == 'M' and tl == tr == 'S':
                count += 1

print(count)

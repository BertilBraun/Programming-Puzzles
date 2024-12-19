"""In a grid of 4 by 4 squares you want to place a skyscraper in each square with only some clues:

The height of the skyscrapers is between 1 and 4
No two skyscrapers in a row or column may have the same number of floors
A clue is the number of skyscrapers that you can see in a row or column from the outside
Higher skyscrapers block the view of lower skyscrapers located behind them

Can you write a program that can solve this puzzle?

Example:

To understand how the puzzle works, this is an example of a row with 2 clues. Seen from the left side there are 4 buildings visible while seen from the right side only 1:

 4	    	    	    	    	 1

There is only one way in which the skyscrapers can be placed. From left-to-right all four buildings must be visible and no building may hide behind another building:

 4	 1	 2	 3	 4	 1

Example of a 4 by 4 puzzle with the solution:

  	    	    	 1	 2	  
  	  	  	  	  	  
  	  	  	  	  	 2
 1	  	  	  	  	  
  	  	  	  	  	  
  	  	  	 3	  	  

  	  	  	 1	 2	  
  	 2	 1	 4	 3	  
  	 3	 4	 1	 2	 2
 1	 4	 2	 3	 1	  
  	 1	 3	 2	 4	  
  	  	  	 3	  	  

Task:

Finish:
public static int[][] SolvePuzzle(int[] clues)
Pass the clues in an array of 16 items. This array contains the clues around the clock, index:
  	 0	 1	   2	   3	  
 15	  	  	  	  	 4
 14	  	  	  	  	 5
 13	  	  	  	  	 6
 12	  	  	  	  	 7
  	11	10	 9	 8	  
If no clue is available, add value `0`
Each puzzle has only one possible solution
`SolvePuzzle()` returns matrix `int[][]`. The first indexer is for the row, the second indexer for the column.
"""

from itertools import permutations
from typing import Iterable, Set


def print_board(grid, clues):
    grid_size = len(grid)

    # Print top clues
    print('   ', ' '.join(str(x) for x in clues[:grid_size]))

    # Print rows with left and right clues
    for i in range(grid_size):
        left_clue = clues[4 * grid_size - 1 - i]
        right_clue = clues[grid_size + i]
        print(left_clue, ' ', ' '.join(str(x) for x in grid[i]), ' ', right_clue)

    # Print bottom clues
    bottom_clues = clues[3 * grid_size - 1 : 2 * grid_size - 1 : -1]
    print('   ', ' '.join(str(x) for x in bottom_clues))
    print()


def calculate_lookup_table_index(buildings: Iterable[int], clue: int) -> int:
    lookup_table_index = 0
    lookup_table_index <<= 3
    lookup_table_index += clue
    for b in buildings:
        lookup_table_index <<= 3
        lookup_table_index += b
    return lookup_table_index


def is_lookup_true(buildings: Iterable[int], clue: int) -> bool:
    if clue == 0:
        return True

    num_visible = 0
    max_height = 0
    for building in buildings:
        if building > max_height:
            num_visible += 1
            max_height = building

    return num_visible == clue


def precalculate_lookup_table(grid_size: int) -> dict[int, bool]:
    def gen(place_n: int, num: int, buildings: list[int], num_zeros: int):
        if place_n == 0:
            for clue in range(1, grid_size + 1):
                key = calculate_lookup_table_index(buildings, clue)
                if num_zeros == 0:
                    lookup_table[key] = is_lookup_true(buildings, clue)
                else:
                    zero_index = buildings.index(0)
                    for i in range(1, grid_size + 1):
                        if i in buildings:
                            continue
                        new_key = key + (i << (3 * (grid_size - 1 - zero_index)))

                        if lookup_table.get(new_key, False):
                            lookup_table[key] = True
                            break

        n_remaining = grid_size - num + 1

        for p in range(grid_size):
            if buildings[p] == 0:
                for num_place in range(num, num + n_remaining):
                    buildings[p] = num_place
                    gen(place_n - 1, num_place + 1, buildings, num_zeros)
                    buildings[p] = 0

    lookup_table: dict[int, bool] = {}

    for n in range(grid_size, 0, -1):
        gen(n, 1, [0] * grid_size, grid_size - n)

    return lookup_table


def solve_puzzle(clues: list[int], grid_size: int = 7) -> Iterable[Iterable[int]]:
    def get_col(grid: list[list[int]], col: int) -> list[int]:
        return [grid[row][col] for row in range(grid_size)]

    def get_row(grid: list[list[int]], row: int) -> list[int]:
        return grid[row]

    def entries_from_direction(grid: list[list[int]], row: int, col: int, direction: str) -> Iterable[int]:
        # Check if placing a building at a given position breaks the clue.
        if direction == 'left':
            return get_row(grid, row)
        elif direction == 'right':
            return reversed(get_row(grid, row))
        elif direction == 'up':
            return get_col(grid, col)
        elif direction == 'down':
            return reversed(get_col(grid, col))
        assert False

    def does_break_count(values: list[int]) -> bool:
        # Check if placing a building at a given position breaks the count.
        counts = [0] * (grid_size)
        for value in values:
            if value != 0:
                counts[value - 1] += 1
        return any(count > 1 for count in counts)

    def does_break(grid: list[list[int]], row: int, col: int) -> bool:
        # Check if placing a building at a given position breaks the clues.

        if does_break_count(get_row(grid, row)) or does_break_count(get_col(grid, col)):
            return True

        for dir, clue in zip(DIRS, grid_clues[row][col]):
            if clue == 0:
                continue

            entries = entries_from_direction(grid, row, col, dir)
            if not access_lookup_table(calculate_lookup_table_index(entries, clue)):
                return True

        return False

    def is_grid_broken(grid: list[list[int]]) -> bool:
        for row in range(grid_size):
            for col in range(grid_size):
                if does_break(grid, row, col):
                    return True
        return False

    def solve_puzzle_helper(grid: list[list[int]], lookup_index: int) -> bool:
        # Recursive function to solve the puzzle using backtracking.
        # print_board(grid, clues)
        if lookup_index == len(lookup_order):
            return True

        # get most constrained cell instead of continuning the lookup order

        _, row, col = lookup_order[lookup_index]

        if grid[row][col] != 0:
            return solve_puzzle_helper(grid, lookup_index + 1)

        # set fixed heights if they can be directly inferred
        rows: list[Set[int]] = [set() for _ in range(grid_size)]
        cols: list[Set[int]] = [set() for _ in range(grid_size)]

        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] != 0:
                    rows[r].add(grid[r][c])
                    cols[c].add(grid[r][c])

        print('Rows:', rows)
        print('Cols:', cols)

        all_nums = set(range(1, grid_size + 1))

        for r, row_nums in enumerate(rows):
            if len(row_nums) == grid_size - 1:
                num = (all_nums - row_nums).pop()
                for c in range(grid_size):
                    if grid[r][c] == 0:
                        print('Setting Row:', r, c, num)
                        grid[r][c] = num
                        row_nums.add(num)
                        if does_break(grid, r, c):
                            grid[r][c] = 0
                            return False
                        break

        for c, col_nums in enumerate(cols):
            if len(col_nums) == grid_size - 1:
                num = (all_nums - col_nums).pop()
                for r in range(grid_size):
                    if grid[r][c] == 0:
                        print('Setting Col:', r, c, num)
                        grid[r][c] = num
                        col_nums.add(num)
                        if does_break(grid, r, c):
                            grid[r][c] = 0
                            return False
                        break

        for r in range(grid_size):
            for c in range(grid_size):
                intersections = all_nums - (rows[r] | cols[c])
                if len(intersections) == 1:
                    print('Setting Intersection:', r, c, intersections)
                    grid[r][c] = intersections.pop()
                    if does_break(grid, r, c):
                        grid[r][c] = 0
                        return False

        assert not is_grid_broken(grid)
        if grid[row][col] != 0:
            return solve_puzzle_helper(grid, lookup_index + 1)

        # TODO for height in (all_nums - (rows[row] | cols[col])):

        for height in range(grid_size, 0, -1):
            grid[row][col] = height
            if not does_break(grid, row, col) and solve_puzzle_helper(grid, lookup_index + 1):
                return True

        grid[row][col] = 0
        return False

    # for each cell, keep track of the 4 clues that are visible from that cell
    # up, right, down, left
    DIRS = ('up', 'down', 'left', 'right')
    grid_clues = [
        [
            (
                clues[col],
                clues[3 * grid_size - 1 - col],
                clues[4 * grid_size - 1 - row],
                clues[grid_size + row],
            )
            for col in range(grid_size)
        ]
        for row in range(grid_size)
    ]

    lookup_order = [
        (sum(clue for clue in grid_clues[row][col]) + 1, row, col)
        for row in range(grid_size)
        for col in range(grid_size)
    ]
    lookup_order.sort(reverse=True)
    # lookup_order = [(l**4, *a) for l, *a in lookup_order]
    # actual_lookup_order = []
    # while lookup_order:
    #     # sample from lookup order with the constraints as probabilities
    #     lookup_order_sum = sum(x for x, *_ in lookup_order)
    #     props = [x / lookup_order_sum for x, *_ in lookup_order]
    #     r = random.random()
    #     for i, p in enumerate(props):
    #         if r < p:
    #             actual_lookup_order.append(lookup_order.pop(i))
    #             break
    #         r -= p
    #     else:
    #         raise Exception('This should never happen')
    #
    # lookup_order = actual_lookup_order

    # random.shuffle(lookup_order)
    # lookup_order = [(0, row, col) for row in range(grid_size) for col in range(grid_size)]

    for indices in permutations(range(grid_size)):
        grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        for i, index in enumerate(indices):
            grid[i][index] = grid_size

        if is_grid_broken(grid):
            continue

        print('Trying:', indices)
        print_board(grid, clues)
        if solve_puzzle_helper(grid, 0):
            return grid

    return grid


lookup_table = precalculate_lookup_table(7)


def access_lookup_table(index):
    return lookup_table.get(index, False)


def assert_equals(a, b, clues):
    print('Testing:')
    a = list(list(row) for row in a)
    b = list(list(row) for row in b)
    print_board(a, clues)
    print_board(b, clues)
    assert all(row == expected_row for row, expected_row in zip(a, b))


if False:
    expected = [
        [2, 1, 4, 3],
        [3, 4, 1, 2],
        [4, 2, 3, 1],
        [1, 3, 2, 4],
    ]
    clues = [0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0]
    res = solve_puzzle(clues, 4)
    print(res)
    assert_equals(res, expected, clues)

    expected = [
        [5, 6, 1, 4, 3, 2],
        [4, 1, 3, 2, 6, 5],
        [2, 3, 6, 1, 5, 4],
        [6, 5, 4, 3, 2, 1],
        [1, 2, 5, 6, 4, 3],
        [3, 4, 2, 5, 1, 6],
    ]
    clues = [0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0]
    res = solve_puzzle(clues, 6)
    print(res)
    assert_equals(res, expected, clues)


expected = [
    [1, 5, 6, 7, 4, 3, 2],
    [2, 7, 4, 5, 3, 1, 6],
    [3, 4, 5, 6, 7, 2, 1],
    [4, 6, 3, 1, 2, 7, 5],
    [5, 3, 1, 2, 6, 4, 7],
    [6, 2, 7, 3, 1, 5, 4],
    [7, 1, 2, 4, 5, 6, 3],
]
clues = [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]
res = solve_puzzle(clues, 7)
assert_equals(res, expected, clues)

clues = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0]
assert_equals(
    solve_puzzle(clues, 7),  # for a _very_ hard puzzle, replace the last 7 values with zeroes
    [
        [7, 6, 2, 1, 5, 4, 3],
        [1, 3, 5, 4, 2, 7, 6],
        [6, 5, 4, 7, 3, 2, 1],
        [5, 1, 7, 6, 4, 3, 2],
        [4, 2, 1, 3, 7, 6, 5],
        [3, 7, 6, 2, 1, 5, 4],
        [2, 4, 3, 5, 6, 1, 7],
    ],
    clues,
)

clues = [0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3]
assert_equals(
    solve_puzzle(clues, 7),
    [
        [3, 4, 1, 7, 6, 5, 2],
        [7, 1, 2, 5, 4, 6, 3],
        [6, 3, 5, 2, 1, 7, 4],
        [1, 2, 3, 6, 7, 4, 5],
        [5, 7, 6, 4, 2, 3, 1],
        [4, 5, 7, 1, 3, 2, 6],
        [2, 6, 4, 3, 5, 1, 7],
    ],
    clues,
)

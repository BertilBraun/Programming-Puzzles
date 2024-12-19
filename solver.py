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
    lookup_table_index = clue
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
                    if is_lookup_true(buildings, clue):
                        lookup_table[key] = 1
                else:
                    zero_index = buildings.index(0)
                    for i in range(1, grid_size + 1):
                        if i in buildings:
                            continue
                        new_key = key + (i << (3 * (grid_size - 1 - zero_index)))

                        if lookup_table.get(new_key, False):
                            lookup_table[key] = lookup_table.get(key, 0) + 1
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
    result_grid = None
    all_nums = set(range(1, grid_size + 1))

    print("CLUES: ")
    print(clues)

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
        seen = [False] * grid_size
        for value in values:
            if value != 0:
                if seen[value - 1]:  # already seen this value
                    return True
                seen[value - 1] = True
        return False

    def does_break(grid: list[list[int]], row: int, col: int) -> bool:
        # Check if placing a building at a given position breaks the clues.

        if does_break_count(get_row(grid, row)) or does_break_count(get_col(grid, col)):
            return True

        for dir, clue in zip(DIRS, grid_clues[row][col]):
            if clue == 0:
                continue

            entries = entries_from_direction(grid, row, col, dir)
            if not lookup_table.get(calculate_lookup_table_index(entries, clue), False):
                return True

        return False

    def is_grid_broken(grid: list[list[int]]) -> bool:
        for row in range(grid_size):
            for col in range(grid_size):
                if does_break(grid, row, col):
                    return True
        return False

    def solve_puzzle_helper(grid: list[list[int]], rows: list[Set[int]], cols: list[Set[int]], lookup_index: int, row: int, col: int) -> bool:
        # DO NOT MODIFY rows, cols
        nonlocal result_grid

        # Recursive function to solve the puzzle using backtracking.
        # print_board(grid, clues)
        if lookup_index == last_lookup_index:
            result_grid = [list(row) for row in grid]
            return True

        if grid[row][col] != 0:
            return solve_puzzle_helper(grid, rows, cols, lookup_index + 1, row, col)

        # copy grid to avoid modifying the original
        grid = [list(row) for row in grid]
        rows = [set(row) for row in rows]
        cols = [set(col) for col in cols]

        max_constrained_cell = None
        max_constrains_on_cell = -999999999999999

        # Fills every cell that is determined by uniqueness constraints on row + col
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r][c] != 0:
                    continue

                intersections = all_nums - (rows[r] | cols[c])
                l_intersections = len(intersections)
                if l_intersections == 1:
                    num = intersections.pop()
                    grid[r][c] = num
                    rows[r].add(num)
                    cols[c].add(num)
                    lookup_index += 1
                    if does_break(grid, r, c):
                        return False
                else:
                    constraints = -l_intersections
                    for clue in grid_clues[r][c]:
                        constraints += clue
                    if constraints > max_constrains_on_cell:
                        max_constrains_on_cell = constraints
                        max_constrained_cell = (r, c)

        if grid[row][col] != 0:
            return solve_puzzle_helper(grid, rows, cols, lookup_index, max_constrained_cell[0], max_constrained_cell[1])

        row, col = max_constrained_cell
        for height in all_nums - (rows[row] | cols[col]):
            grid[row][col] = height
            if not does_break(grid, row, col):
                rows[row].add(height)
                cols[col].add(height)
                if solve_puzzle_helper(grid, rows, cols, lookup_index + 1, max_constrained_cell[0], max_constrained_cell[1]):
                    return True
                rows[row].remove(height)
                cols[col].remove(height)
        return False

    # ========================================================
    #                    SOLVE PUZZLE FUNCTION
    # ========================================================
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
    last_lookup_index = len(lookup_order)

    # placing all highest buildings before first backtracking iteration
    for indices in permutations(range(grid_size)):
        grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        for i, index in enumerate(indices):
            grid[i][index] = grid_size


        # for r in range(grid_size):
        #     for c in range(grid_size):
        #         grid[r][c] = expected[r][c] if expected[r][c] == 7 else 0  # TODO remove

        if is_grid_broken(grid):
            continue

        set7s = [set([7]) for _ in range(grid_size)]

        # print('Trying:', indices)
        # print_board(grid, clues)
        _, sr, sc = lookup_order[0]
        if solve_puzzle_helper(grid, set7s, set7s, 0, sr, sc):
            return result_grid

        # raise Exception('No solution found')  # TODO remove

    assert False, 'No solution found'


lookup_table = precalculate_lookup_table(7)

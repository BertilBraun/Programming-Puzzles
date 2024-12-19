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

from copy import copy
from itertools import permutations
from typing import Iterable


DEBUG_EXPECTED = True
DEBUG_PRINT = True

global_print = print
global_input = input
print = global_print if DEBUG_PRINT else lambda *args, **kwargs: None
input = global_input if DEBUG_PRINT else lambda *args, **kwargs: None


def print_board(grid, clues):
    grid_size = len(grid)

    # Print top clues
    global_print('   ', ' '.join(str(x) for x in clues[:grid_size]))

    # Print rows with left and right clues
    for i in range(grid_size):
        left_clue = clues[4 * grid_size - 1 - i]
        right_clue = clues[grid_size + i]
        global_print(left_clue, ' ', ' '.join(str(x) for x in grid[i]), ' ', right_clue)

    # Print bottom clues
    bottom_clues = clues[3 * grid_size - 1 : 2 * grid_size - 1 : -1]
    global_print('   ', ' '.join(str(x) for x in bottom_clues))
    global_print()


def calculate_lookup_table_index(buildings: Iterable[int], clue: int) -> int:
    lookup_table_index = 0
    for b in buildings:
        lookup_table_index <<= 3
        lookup_table_index += b
    lookup_table_index <<= 3
    lookup_table_index += clue
    return lookup_table_index


def is_lookup_true(buildings: Iterable[int], clue: int) -> bool:
    # print('Checking:', buildings, clue)
    num_visible = 0
    max_height = 0
    for building in buildings:
        if building > max_height:
            num_visible += 1
            max_height = building
    return num_visible == clue


def precalculate_lookup_table(grid_size: int) -> dict[int, bool]:
    lookup_table = {}

    def gen(place_n, num, buildings, num_zeros):
        # print(place_n, num, perm)
        if place_n == 0:
            for clue in range(1, grid_size + 1):
                if num_zeros == 0:
                    lookup_table[calculate_lookup_table_index(buildings, clue)] = is_lookup_true(buildings, clue)
                else:
                    zero_index = buildings.index(0)
                    key = calculate_lookup_table_index(buildings, clue)
                    for i in range(1, grid_size + 1):
                        if i in buildings:
                            continue
                        buildings[zero_index] = i
                        # print('Lookup', buildings, clue)
                        if lookup_table[calculate_lookup_table_index(buildings, clue)]:
                            lookup_table[key] = True
                            break
                    else:
                        lookup_table[key] = False

                    buildings[zero_index] = 0

        n_remaining = grid_size - num + 1

        for p in range(grid_size):
            if buildings[p] == 0:
                for num_place in range(num, num + n_remaining):
                    buildings[p] = num_place
                    gen(place_n - 1, num_place + 1, buildings, num_zeros)
                    buildings[p] = 0

    valid_buildings = list(range(1, grid_size + 1))
    for clue in range(1, grid_size + 1):
        for buildings in permutations(valid_buildings):
            lookup_table[calculate_lookup_table_index(buildings, clue)] = is_lookup_true(buildings, clue)

    for n in range(grid_size, 0, -1):
        gen(n, 1, [0] * grid_size, grid_size - n)

    return lookup_table
    """

    valid_buildings = list(range(1, grid_size + 1))
    for clue in range(1, grid_size + 1):
        for buildings in permutations(valid_buildings):
            lookup_table[calculate_lookup_table_index(buildings, clue)] = is_lookup_true(buildings, clue)
            # print('Initial', buildings, clue, lookup_table[calculate_lookup_table_index(buildings, clue)])

    def recurse(buildings, index, clue):
        if index == grid_size:
            return

        new_buildings = buildings.copy()
        new_buildings[index] = 0
        key = calculate_lookup_table_index(new_buildings, clue)

        for i in range(1, grid_size + 1):
            buildings[index] = i
            if lookup_table[calculate_lookup_table_index(buildings, clue)]:
                lookup_table[key] = True
                break

    num = 0
    for i in range(1, grid_size):
        for clue in range(1, grid_size + 1):
            for buildings in get(i):
                left_out = [val for val in left_out if val != 0]
                if not left_out:
                    continue
                zero_index = buildings.index(0)
                if zero_index == -1:
                    continue
                result = False
                for v in left_out:
                    new_new_buildings = list(buildings)
                    new_new_buildings[zero_index] = v
                    # print('Checking', new_new_buildings, clue)
                    result = result or lookup_table.get(calculate_lookup_table_index(new_new_buildings, clue), False)
                    if result:
                        break

                num += 1
                lookup_table[calculate_lookup_table_index(buildings, clue)] = result

            # 0, 1, 2, 3, 4 ...
            # (0, 1), (0, 2), (0, 3), (0, 4) ...
            # (0, 1, 2), (0, 1, 3), (0, 1, 4) ...
            # Up to ...
            # (0, 1, 2, 3, 4, 5, 6, ...)
            print(num)

    def fill_lookup_table(buildings: list[int], clue: int, index: int) -> None:
        if index == grid_size:
            lookup_table[calculate_lookup_table_index(buildings, clue)] = is_lookup_true(buildings, clue)
            print('Lookup:', buildings, clue, lookup_table[calculate_lookup_table_index(buildings, clue)])
            return

        for i in range(grid_size + 1):
            buildings[index] = i
            if i > 0 and buildings[:index].count(i) > 0:
                continue
            fill_lookup_table(buildings, clue, index + 1)
            buildings[index] = 0

    # for clue in range(1, grid_size + 1):
    #     buildings = [0] * grid_size
    #     fill_lookup_table(buildings, clue, 0)
    return lookup_table"""


lookup_table = precalculate_lookup_table(7)
print(len(lookup_table))
exit()


def solve_puzzle(clues: list[int], grid_size) -> list[list[int]]:
    # I'm thinking about a backtracking approach to solve this problem.
    # I will start by creating a 4x4 grid with all values set to 0.
    # Then I will try to place the skyscrapers in the grid and check if the clues are satisfied.
    # If the clues are not satisfied, I will backtrack and try a different placement.
    # I will continue this process until a valid solution is found.
    # I will use a recursive function to implement the backtracking algorithm.
    # I will also need helper functions to check the visibility of skyscrapers from different directions.
    # I will start by implementing the helper functions.

    lookup_table = precalculate_lookup_table(grid_size)

    def get_col(grid: list[list[int]], col: int) -> list[int]:
        return [grid[row][col] for row in range(grid_size)]

    def get_row(grid: list[list[int]], row: int) -> list[int]:
        return grid[row]

    def is_valid_row(grid: list[list[int]], row: int) -> bool:
        # Check if the row contains unique values.
        return len(set(get_row(grid, row))) == grid_size

    def is_valid_column(grid: list[list[int]], col: int) -> bool:
        # Check if the column contains unique values.
        return len(set(get_col(grid, col))) == grid_size

    def is_valid_row_clue(grid: list[list[int]], clue: int, row: int, direction: str) -> bool:
        # Check if the row clue is satisfied.
        if clue == 0:
            return True
        if direction == 'left':
            return check_break_clue_min_and_max(get_row(grid, row), clue)
        elif direction == 'right':
            return check_break_clue_min_and_max(get_row(grid, row)[::-1], clue)
        assert False

    def is_valid_column_clue(grid: list[list[int]], clue: int, col: int, direction: str) -> bool:
        # Check if the column clue is satisfied.
        if clue == 0:
            return True
        if direction == 'up':
            return check_break_clue_min_and_max(get_col(grid, col), clue)
        elif direction == 'down':
            return check_break_clue_min_and_max(get_col(grid, col)[::-1], clue)
        assert False

    def count_visible_buildings(buildings: list[int], remaining: list[int]) -> int:
        # Count the number of visible buildings in a row or column.

        visible_buildings = 0
        max_height = 0
        remaining_index = 0

        for building in buildings:
            if building == 0:
                # while remaining_index < len(remaining) and remaining[remaining_index] <
                building = remaining[remaining_index]
                remaining_index += 1
            if building > max_height:
                visible_buildings += 1
                max_height = building

        return visible_buildings

    def check_break_clue_min_and_max(buildings: list[int], clue: int) -> bool:
        # TODO look at both clues for a row/col to break even earlier
        return lookup_table[calculate_lookup_table_index(buildings, clue)]

    def does_break_clue(grid: list[list[int]], row: int, col: int, direction: str, clue: int) -> bool:
        # Check if placing a building at a given position breaks the clue.
        if clue == 0:
            return False
        if direction == 'left':
            return check_break_clue_min_and_max(get_row(grid, row), clue)
        elif direction == 'right':
            return check_break_clue_min_and_max(get_row(grid, row)[::-1], clue)
        elif direction == 'up':
            return check_break_clue_min_and_max(get_col(grid, col), clue)
        elif direction == 'down':
            return check_break_clue_min_and_max(get_col(grid, col)[::-1], clue)
        assert False

    def does_break_count(grid: list[list[int]], row: int, col: int) -> bool:
        # Check if placing a building at a given position breaks the count.
        row_values = get_row(grid, row)
        col_values = get_col(grid, col)
        for i in range(1, grid_size + 1):
            if row_values.count(i) > 1:
                return True
            if col_values.count(i) > 1:
                return True
        return False

    def is_solution(grid: list[list[int]]) -> bool:
        # Check if the grid is a valid solution.
        for i in range(grid_size):
            if not is_valid_column(grid, i):
                return False
            if not is_valid_row(grid, i):
                return False
            if not is_valid_column_clue(grid, clues[i], i, 'up'):
                return False
            if not is_valid_row_clue(grid, clues[4 * grid_size - 1 - i], i, 'left'):
                return False
            if not is_valid_column_clue(grid, clues[3 * grid_size - 1 - i], i, 'down'):
                return False
            if not is_valid_row_clue(grid, clues[grid_size + i], i, 'right'):
                return False
        return True

    def does_break(grid: list[list[int]], row: int, col: int) -> bool:
        # Check if placing a building at a given position breaks the clues.

        # TODO check if we can improve the pruning
        # check by hand
        print('Checking if breaking:', row, col)
        print_board(grid, clues)
        # input('Press enter to continue')

        # TODO also break if the count from min is broken - i.e. if the clue is 1 but the max val is not directly next to it, then the clue is definitely broken - does that work for other clues as well? - if so, how?
        # TODO for maximum size clues, can we infer, that they must be almost sorted? - i.e. if the clue is 4, then the max value must be in the last position, the second highest in the second last position, etc.

        if does_break_count(grid, row, col):  # This should be fine forever
            return True

        for dir, clue in zip(DIRS, grid_clues[row][col]):
            if does_break_clue(grid, row, col, dir, clue):  # This is the problem
                return True

        return False

    def solve_puzzle_helper(grid: list[list[int]], lookup_index: int) -> bool:
        # Recursive function to solve the puzzle using backtracking.
        # print_board(grid, clues)
        if lookup_index == len(lookup_order):
            return True
            return is_solution(grid)

        _, row, col = lookup_order[lookup_index]
        for height in [expected[row][col]] if DEBUG_EXPECTED else range(grid_size, 0, -1):
            if lookup_index < 9:
                print(
                    'Trying lookup index:',
                    lookup_index,
                    'height:',
                    height,
                    'row:',
                    row,
                    'col:',
                    col,
                    'expected:',
                    # expected[row][col],
                )
            grid[row][col] = height
            if not does_break(grid, row, col) and solve_puzzle_helper(grid, lookup_index + 1):
                return True
            else:
                print_board(grid, clues)
                raise Exception('')
        grid[row][col] = 0
        return False

    # for each cell, keep track of the 4 clues that are visible from that cell
    # up, right, down, left
    DIRS = ('up', 'right', 'down', 'left')
    grid_clues = [
        [
            (
                clues[col],
                clues[grid_size + row],
                clues[3 * grid_size - 1 - col],
                clues[4 * grid_size - 1 - row],
            )
            for col in range(grid_size)
        ]
        for row in range(grid_size)
    ]

    # store the grid_size * grid_size moves in order of interest based on how restrictive the clues about a given location are
    # store (num_constraints, row, col) tuples
    lookup_order = [(sum(grid_clues[row][col]), row, col) for row in range(grid_size) for col in range(grid_size)]
    lookup_order.sort(reverse=True)
    # lookup_order = [(0, row, col) for row in range(grid_size) for col in range(grid_size)]

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    solve_puzzle_helper(grid, 0)
    return grid


def assert_equals(a, b, clues):
    global_print('Testing:')
    print_board(a, clues)
    print_board(b, clues)
    assert all(row == expected_row for row, expected_row in zip(a, b))


expected = [
    [2, 1, 4, 3],
    [3, 4, 1, 2],
    [4, 2, 3, 1],
    [1, 3, 2, 4],
]
clues = [0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0]
res = solve_puzzle(clues, 4)
global_print(res)
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
global_print(res)
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
global_print(res)
assert_equals(res, expected, clues)

exit()
assert_equals(
    solve_puzzle([0, 0, 5, 0, 0, 0, 6, 4, 0, 0, 2, 0, 2, 0, 0, 5, 2, 0, 0, 0, 5, 0, 3, 0, 5, 0, 0, 3], 7),
    [
        [3, 4, 1, 7, 6, 5, 2],
        [7, 1, 2, 5, 4, 6, 3],
        [6, 3, 5, 2, 1, 7, 4],
        [1, 2, 3, 6, 7, 4, 5],
        [5, 7, 6, 4, 2, 3, 1],
        [4, 5, 7, 1, 3, 2, 6],
        [2, 6, 4, 3, 5, 1, 7],
    ],
)

assert_equals(
    solve_puzzle(
        [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1], 7
    ),  # for a _very_ hard puzzle, replace the last 7 values with zeroes
    [
        [7, 6, 2, 1, 5, 4, 3],
        [1, 3, 5, 4, 2, 7, 6],
        [6, 5, 4, 7, 3, 2, 1],
        [5, 1, 7, 6, 4, 3, 2],
        [4, 2, 1, 3, 7, 6, 5],
        [3, 7, 6, 2, 1, 5, 4],
        [2, 4, 3, 5, 6, 1, 7],
    ],
)

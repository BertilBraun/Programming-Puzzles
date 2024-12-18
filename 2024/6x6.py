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


def print_board(grid, clues):
    print('   ', clues[0], clues[1], clues[2], clues[3])
    print(clues[15], ' ', ' '.join(str(x) for x in grid[0]), ' ', clues[4])
    print(clues[14], ' ', ' '.join(str(x) for x in grid[1]), ' ', clues[5])
    print(clues[13], ' ', ' '.join(str(x) for x in grid[2]), ' ', clues[6])
    print(clues[12], ' ', ' '.join(str(x) for x in grid[3]), ' ', clues[7])
    print('   ', clues[11], clues[10], clues[9], clues[8])
    print()


def solve_puzzle(clues: list[int], grid_size) -> list[list[int]]:
    # I'm thinking about a backtracking approach to solve this problem.
    # I will start by creating a 4x4 grid with all values set to 0.
    # Then I will try to place the skyscrapers in the grid and check if the clues are satisfied.
    # If the clues are not satisfied, I will backtrack and try a different placement.
    # I will continue this process until a valid solution is found.
    # I will use a recursive function to implement the backtracking algorithm.
    # I will also need helper functions to check the visibility of skyscrapers from different directions.
    # I will start by implementing the helper functions.

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
            visible_buildings = count_visible_buildings(get_row(grid, row))
        elif direction == 'right':
            visible_buildings = count_visible_buildings(get_row(grid, row)[::-1])
        return visible_buildings == clue

    def is_valid_column_clue(grid: list[list[int]], clue: int, col: int, direction: str) -> bool:
        # Check if the column clue is satisfied.
        if clue == 0:
            return True
        if direction == 'up':
            visible_buildings = count_visible_buildings(get_col(grid, col))
        elif direction == 'down':
            visible_buildings = count_visible_buildings(get_col(grid, col)[::-1])
        return visible_buildings == clue

    def count_visible_buildings(buildings: list[int]) -> int:
        # Count the number of visible buildings in a row or column.
        remaining = set(range(1, grid_size + 1)) - set(buildings)
        max_remaining = max(remaining, default=0)
        visible_buildings = 0
        max_height = 0
        for building in buildings:
            if building == 0:
                building = max_remaining
            if building > max_height:
                visible_buildings += 1
                max_height = building
        return visible_buildings

    def does_break_clue(grid: list[list[int]], row: int, col: int, direction: str, clue: int) -> bool:
        # Check if placing a building at a given position breaks the clue.
        if clue == 0:
            return False
        if direction == 'left':
            visible_buildings = count_visible_buildings(get_row(grid, row))
        elif direction == 'right':
            visible_buildings = count_visible_buildings(get_row(grid, row)[::-1])
        elif direction == 'up':
            visible_buildings = count_visible_buildings(get_col(grid, col))
        elif direction == 'down':
            visible_buildings = count_visible_buildings(get_col(grid, col)[::-1])
        return visible_buildings > clue

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
        input('Press enter to continue')

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
            return is_solution(grid)

        _, row, col = lookup_order[lookup_index]
        for height in range(grid_size, 0, -1):
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
                    expected[row][col],
                )
            grid[row][col] = height
            if does_break(grid, row, col):
                continue

            if solve_puzzle_helper(grid, lookup_index + 1):
                return True

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
    print('Lookup order:')
    for i, (num_constraints, row, col) in enumerate(lookup_order):
        print(i, num_constraints, row, col)

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    solve_puzzle_helper(grid, 0)
    return grid


# Test cases


def assert_equals(a, b):
    assert all(row == expected_row for row, expected_row in zip(a, b))


expected = [
    [2, 1, 4, 3],
    [3, 4, 1, 2],
    [4, 2, 3, 1],
    [1, 3, 2, 4],
]
res = solve_puzzle([0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0], 4)
print(res)
assert_equals(res, expected)


expected = [
    [5, 6, 1, 4, 3, 2],
    [4, 1, 3, 2, 6, 5],
    [2, 3, 6, 1, 5, 4],
    [6, 5, 4, 3, 2, 1],
    [1, 2, 5, 6, 4, 3],
    [3, 4, 2, 5, 1, 6],
]
res = solve_puzzle([0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 3, 0, 0, 4, 0, 0, 0, 0, 4, 4, 0, 3, 0, 0], 6)
print(res)
assert_equals(res, expected)

exit()


assert_equals(
    solve_puzzle([7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4], 7),
    [
        [1, 5, 6, 7, 4, 3, 2],
        [2, 7, 4, 5, 3, 1, 6],
        [3, 4, 5, 6, 7, 2, 1],
        [4, 6, 3, 1, 2, 7, 5],
        [5, 3, 1, 2, 6, 4, 7],
        [6, 2, 7, 3, 1, 5, 4],
        [7, 1, 2, 4, 5, 6, 3],
    ],
)

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

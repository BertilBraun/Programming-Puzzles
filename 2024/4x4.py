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


def SolvePuzzle(clues: list[int]) -> list[list[int]]:
    # I'm thinking about a backtracking approach to solve this problem.
    # I will start by creating a 4x4 grid with all values set to 0.
    # Then I will try to place the skyscrapers in the grid and check if the clues are satisfied.
    # If the clues are not satisfied, I will backtrack and try a different placement.
    # I will continue this process until a valid solution is found.
    # I will use a recursive function to implement the backtracking algorithm.
    # I will also need helper functions to check the visibility of skyscrapers from different directions.
    # I will start by implementing the helper functions.

    def is_valid_row(grid: list[list[int]], row: int) -> bool:
        # Check if the row contains unique values.
        row_values = grid[row]
        return len(set(row_values)) == 4

    def is_valid_column(grid: list[list[int]], col: int) -> bool:
        # Check if the column contains unique values.
        col_values = [grid[row][col] for row in range(4)]
        return len(set(col_values)) == 4

    def is_valid_row_clue(grid: list[list[int]], clue: int, row: int, direction: str) -> bool:
        # Check if the row clue is satisfied.
        if clue == 0:
            return True
        if direction == 'left':
            visible_buildings = count_visible_buildings(grid[row])
        elif direction == 'right':
            visible_buildings = count_visible_buildings(grid[row][::-1])
        return visible_buildings == clue

    def is_valid_column_clue(grid: list[list[int]], clue: int, col: int, direction: str) -> bool:
        # Check if the column clue is satisfied.
        if clue == 0:
            return True
        if direction == 'up':
            visible_buildings = count_visible_buildings([grid[row][col] for row in range(4)])
        elif direction == 'down':
            visible_buildings = count_visible_buildings([grid[row][col] for row in range(4)][::-1])
        return visible_buildings == clue

    def count_visible_buildings(buildings: list[int]) -> int:
        # Count the number of visible buildings in a row or column.
        visible_buildings = 0
        max_height = 0
        for building in buildings:
            if building > max_height:
                visible_buildings += 1
                max_height = building
        return visible_buildings

    def does_break_clue(grid: list[list[int]], row: int, col: int, direction: str, clue: int) -> bool:
        # Check if placing a building at a given position breaks the clue.
        if clue == 0:
            return False
        print('Does break clue:', grid, row, col, direction, clue)
        if direction == 'left':
            visible_buildings = count_visible_buildings(grid[row])
        elif direction == 'right':
            visible_buildings = count_visible_buildings(grid[row][::-1])
        elif direction == 'up':
            visible_buildings = count_visible_buildings([grid[row][col] for row in range(4)])
        elif direction == 'down':
            visible_buildings = count_visible_buildings([grid[row][col] for row in range(4)][::-1])
        return visible_buildings > clue

    def does_break_count(grid: list[list[int]], row: int, col: int) -> bool:
        # Check if placing a building at a given position breaks the count.
        row_values = grid[row]
        col_values = [grid[row][col] for row in range(4)]
        for i in range(1, 5):
            if row_values.count(i) > 1:
                return True
            if col_values.count(i) > 1:
                return True
        return False

    def is_solution(grid: list[list[int]]) -> bool:
        # Check if the grid is a valid solution.
        for i in range(4):
            if not is_valid_column(grid, i):
                return False
            if not is_valid_row(grid, i):
                return False
            if not is_valid_column_clue(grid, clues[i], i, 'up'):
                return False
            if not is_valid_row_clue(grid, clues[15 - i], i, 'left'):
                return False
            if not is_valid_column_clue(grid, clues[11 - i], i, 'down'):
                return False
            if not is_valid_row_clue(grid, clues[4 + i], i, 'right'):
                return False
        return True

    def solve_puzzle_helper(grid: list[list[int]], row: int, col: int) -> bool:
        # Recursive function to solve the puzzle using backtracking.
        if row == 4:
            print('Trying solution:', grid)
            return is_solution(grid)

        next_row = row + 1 if col == 3 else row
        next_col = (col + 1) % 4
        for height in range(1, 5):
            grid[row][col] = height
            if does_break_count(grid, row, col):
                continue
            if does_break_clue(grid, row, col, 'up', clues[col]):
                continue
            if does_break_clue(grid, row, col, 'left', clues[15 - row]):
                continue
            if does_break_clue(grid, row, col, 'right', clues[4 + row]):
                continue
            if does_break_clue(grid, row, col, 'down', clues[11 - col]):
                continue

            if solve_puzzle_helper(grid, next_row, next_col):
                return True
        grid[row][col] = 0
        return False

    grid = [[0 for _ in range(4)] for _ in range(4)]
    solve_puzzle_helper(grid, 0, 0)
    return grid


# Test cases

expected = [2, 1, 4, 3, 3, 4, 1, 2, 4, 2, 3, 1, 1, 3, 2, 4]
res = SolvePuzzle([0, 0, 1, 2, 0, 2, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0])
print(res)
print('Correct:', res == expected)

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

from typing import Iterable, Set


LOOKUP_TABLE_NUMS = []


DEBUG_EXPECTED = False
DEBUG_PRINT = False
GENERATE_LOOKUP_TABLE = False

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


def calculate_lookup_table_index(buildings: Iterable[int], clue_start: int, clue_end: int) -> int:
    lookup_table_index = 0
    lookup_table_index <<= 3
    lookup_table_index += clue_start
    lookup_table_index <<= 3
    lookup_table_index += clue_end
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


def precalculate_lookup_table(grid_size: int, all_clues: Set[tuple[int, int]]) -> dict[int, tuple[bool, Set[int]]]:
    lookup_table = {}

    def gen(place_n, num, buildings, num_zeros):
        # print(place_n, num, perm)
        if place_n == 0:
            for cs, ce in all_clues:
                key = calculate_lookup_table_index(buildings, cs, ce)
                if num_zeros == 0:
                    if is_lookup_true(buildings, cs) and is_lookup_true(reversed(buildings), ce):
                        lookup_table[key] = True, set()
                else:
                    zero_index = buildings.index(0)
                    possibilities = set()
                    success = False

                    for i in range(1, grid_size + 1):
                        if i in buildings:
                            continue
                        new_key = key + (i << (3 * (grid_size - 1 - zero_index)))
                        succ, poss = lookup_table.get(new_key, (False, set()))

                        if succ:
                            success = True
                            possibilities |= poss
                            possibilities.add(i)
                            if len(possibilities) == num_zeros:
                                break

                    if success:
                        global_print('Adding:', buildings, cs, ce, possibilities)
                        lookup_table[key] = True, possibilities

        n_remaining = grid_size - num + 1

        for p in range(grid_size):
            if buildings[p] == 0:
                for num_place in range(num, num + n_remaining):
                    buildings[p] = num_place
                    gen(place_n - 1, num_place + 1, buildings, num_zeros)
                    buildings[p] = 0

    for n in range(grid_size, 0, -1):
        gen(n, 1, [0] * grid_size, grid_size - n)

    return lookup_table


def solve_puzzle(clues: list[int], grid_size=7) -> Iterable[Iterable[int]]:
    def get_col(grid: list[list[int]], col: int) -> list[int]:
        return [grid[row][col] for row in range(grid_size)]

    def get_row(grid: list[list[int]], row: int) -> list[int]:
        return grid[row]

    def entries_from_direction(grid: list[list[int]], row: int, col: int, direction: str) -> list[int]:
        # Check if placing a building at a given position breaks the clue.
        if direction == 'left-right':
            return get_row(grid, row)
        elif direction == 'up-down':
            return get_col(grid, col)
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

    def does_break(grid: list[list[int]], row: int, col: int) -> tuple[bool, Set[int]]:
        # Check if placing a building at a given position breaks the clues.

        # TODO check if we can improve the pruning
        # check by hand
        print('Checking if breaking:', row, col)
        if DEBUG_PRINT:
            print_board(grid, clues)
        # input('Press enter to continue')

        # TODO also break if the count from min is broken - i.e. if the clue is 1 but the max val is not directly next to it, then the clue is definitely broken - does that work for other clues as well? - if so, how?
        # TODO for maximum size clues, can we infer, that they must be almost sorted? - i.e. if the clue is 4, then the max value must be in the last position, the second highest in the second last position, etc.

        if does_break_count(grid, row, col):  # This should be fine forever
            return True, set()

        all_possible = set(range(1, grid_size + 1))
        for dir, (cs, ce) in zip(DIRS, grid_clues[row][col]):
            if cs == 0 and ce == 0:
                continue
            entries = entries_from_direction(grid, row, col, dir)
            if cs > ce:
                cs, ce = ce, cs
                entries = reversed(entries)
            entries = list(entries)
            # if not access_lookup_table(calculate_lookup_table_index(entries, cs, ce)):
            #    return True

            possibles = set()

            if cs != 0:
                succ, poss = access_lookup_table(calculate_lookup_table_index(reversed(entries), 0, cs))
                if not succ:
                    return True, set()

                possibles |= poss

            if ce != 0:
                succ, poss = access_lookup_table(calculate_lookup_table_index(entries, 0, ce))
                if not succ:
                    return True, set()

                possibles |= poss

            if len(possibles) == 0:
                return True, set()

            all_possible &= possibles

        return False, all_possible

    def solve_puzzle_helper(grid: list[list[int]]) -> bool:
        # Recursive function to solve the puzzle using backtracking.
        # print_board(grid, clues)
        zero_indices = []
        for row in range(grid_size):
            for col in range(grid_size):
                if grid[row][col] == 0:
                    zero_indices.append((row, col))

        if not zero_indices:
            return True

        possibliities = [(row, col, does_break(grid, row, col)) for row, col in zero_indices]
        possibliities = [(row, col, poss[1]) for row, col, poss in possibliities if not poss[0]]
        if not possibliities:
            return False
        possibliities.sort(key=lambda x: len(x[2]))

        # get most constrained cell instead of continuning the lookup order
        for row, col, possible_values in possibliities:
            for height in possible_values:
                grid[row][col] = height
                if solve_puzzle_helper(grid):
                    return True
            grid[row][col] = 0
        return False

        # for height in [expected[row][col]] if DEBUG_EXPECTED else range(grid_size, 0, -1):
        #     grid[row][col] = height
        #     if not does_break(grid, row, col) and solve_puzzle_helper(grid, lookup_index + 1):
        #         return True
        #     elif DEBUG_EXPECTED:
        #         print_board(grid, clues)
        #         raise Exception('')
        # grid[row][col] = 0
        # return False

    # for each cell, keep track of the 4 clues that are visible from that cell
    # up, right, down, left
    DIRS = ('up-down', 'left-right')
    grid_clues = [
        [
            (
                (clues[col], clues[3 * grid_size - 1 - col]),
                (clues[4 * grid_size - 1 - row], clues[grid_size + row]),
            )
            for col in range(grid_size)
        ]
        for row in range(grid_size)
    ]

    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    solve_puzzle_helper(grid)

    if grid_size == 6:
        return tuple(tuple(row) for row in grid)
    return grid


all_clues = set()
for i in range(8):
    all_clues.add((0, i))
all_clues.remove((0, 0))
lookup_table = precalculate_lookup_table(4, all_clues)
global_print('Lookup table generated', len(lookup_table))
global_print(lookup_table)

exit()


def access_lookup_table(index) -> tuple[bool, Set[int]]:
    return lookup_table.get(index, (False, set()))


def assert_equals(a, b, clues):
    global_print('Testing:')
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
assert_equals(res, expected, clues)

clues = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1]
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

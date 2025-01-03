import os
import sys

assert len(sys.argv) == 2, 'Usage: python day.py <day_number>'

day = sys.argv[1]

assert day.isdigit(), 'Day number must be a number'
assert 1 <= int(day) <= 25, 'Day number must be between 1 and 25'

# padd the day number with 0 if it is less than 10
file_day = day.zfill(2)

if os.path.exists(f'{file_day}.py'):
    print(f'Files {file_day}.py already exist')
    if input('Do you want to overwrite it? (YES/NO): ').lower() != 'yes':
        exit()

with open(f'{file_day}.py', 'w') as f:
    f.write(
        f"""from aoc import *
from util import *
from intcode import *


def solve_part1(input: str) -> str | int | None:
    # Your code for part 1 here
    pass


def solve_part2(input: str) -> str | int | None:
    # Your code for part 2 here
    pass


if __name__ == '__main__':
    aoc(day={day}, solve1=solve_part1, solve2=solve_part2, example=False)
"""
    )
print(f'Created {file_day}.py')

import os
import sys

from util import open_day_in_browser, open_file_in_editor

assert len(sys.argv) == 2, 'Usage: python day.py <day_number>'

day = sys.argv[1]

assert day.isdigit(), 'Day number must be a number'
assert 1 <= int(day) <= 25, 'Day number must be between 1 and 25'

# padd the day number with 0 if it is less than 10
file_day = day.zfill(2)

if os.path.exists(f'{file_day}.1.py'):
    print(f'Files {file_day}.1.py already exist')
    if input('Do you want to overwrite it? (YES/NO): ').lower() != 'yes':
        exit()

with open(f'{file_day}.1.py', 'w') as f:
    f.write(
        f"""from aoc import *
from util import *


def solve1(input: str) -> str | int | None:
    pass


if __name__ == '__main__':
    aoc(day={day}, part=1, solve1=solve1, example=False)
"""
    )
print(f'Created {file_day}.1.py')

# open the file in the editor
open_file_in_editor(f'{file_day}.1.py')

# open the day in the browser
year = int(os.path.basename(os.getcwd()))
open_day_in_browser(int(day), year)

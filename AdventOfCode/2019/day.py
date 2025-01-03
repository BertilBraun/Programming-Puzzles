import os


day = input('Enter the day number: ')

assert day.isdigit(), 'Day number must be a number'
assert 1 <= int(day) <= 25, 'Day number must be between 1 and 25'

# padd the day number with 0 if it is less than 10
file_day = day.zfill(2)

if os.path.exists(f'{file_day}.1.py') or os.path.exists(f'{file_day}.2.py'):
    print(f'Files {file_day}.1.py and {file_day}.2.py already exist')
    if input('Do you want to overwrite them? (YES/NO): ').lower() != 'yes':
        exit()

with open(f'{file_day}.1.py', 'w') as f:
    f.write(
        f"""from aoc import *
from util import *
from intcode import *

DAY = {day}
EXAMPLE = False # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day={day})
else:
    input = get_input(day={day})


def solve(input: str) -> str | int | None:
    # Your code here
    pass


if EXAMPLE:
    print(solve(input))
else:
    submit(day={day}, part=1, answer=solve(input))"""
    )
print(f'Created {file_day}.1.py')

with open(f'{file_day}.2.py', 'w') as f:
    f.write(
        f"""from aoc import *
from util import *
from intcode import *

DAY = {day}
EXAMPLE = False # Change to True to solve the example input

if EXAMPLE:
    input = get_example(day={day})
else:
    input = get_input(day={day})
    
    
def solve(input: str) -> str | int | None:
    # Your code here
    pass
    
    
if EXAMPLE:
    print(solve(input))
else:
    submit(day={day}, part=2, answer=solve(input))"""
    )
print(f'Created {file_day}.2.py')

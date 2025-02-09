"""
Advent of Code automation template - @MathisHammel

This template provides functions to download inputs and submit answers on AoC.

You need to paste your adventofcode.com session cookie below.
If you don't know how to get this cookie, here's a quick tutorial:
- Open your browser and go to adventofcode.com, make sure you are logged in
- Open the developer console (Ctrl+Shift+I on Firefox/Chrome)
- Get the value of your session cookie:
      - Chrome : 'Application' tab > Cookies
      - Firefox : 'Storage' tab > Cookies
- The cookie is a string of 96 hexadecimal characters, paste it in the AOC_COOKIE below.

Your cookie is similar to a password, >>> DO NOT SHARE/PUBLISH IT <<<
If you intend to share your solutions, store it in an env variable or a file.
"""

import json
import os
import sys
import requests
from typing import Literal, Callable

from util import open_day_in_browser, open_file_in_editor

with open('cookie.txt') as f:
    AOC_COOKIE = f.read().strip()
YEAR = 2019


def get_input(day: int, year: int = YEAR) -> str:
    req = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', headers={'cookie': 'session=' + AOC_COOKIE})
    return req.text.strip()


def get_example(day: int, offset: int = 0, year: int = YEAR) -> str:
    req = requests.get(f'https://adventofcode.com/{year}/day/{day}', headers={'cookie': 'session=' + AOC_COOKIE})
    return req.text.split('<pre><code>')[offset + 1].split('</code></pre>')[0].strip()


def aoc(
    day: int,
    part: Literal[1, 2] | None = None,
    solve1: Callable[[str], str | int | None] | None = None,
    solve2: Callable[[str], str | int | None] | None = None,
    example: bool = False,
    example_input: str | None = None,
    year: int = YEAR,
) -> None:
    if part is None:
        assert len(sys.argv) == 2 and sys.argv[1] in ('1', '2'), 'Usage: python {{day}}.py <1|2>'

        part = int(sys.argv[1])  # type: ignore
    assert part in (1, 2), 'Part must be 1 or 2'

    if example:
        if example_input is None:
            example_input = get_example(day)
        input_str = example_input
    else:
        input_str = get_input(day)

    if part == 1:
        assert solve1 is not None, 'You need to provide a function to solve part 1'
        solve = solve1(input_str)
    else:
        assert solve2 is not None, 'You need to provide a function to solve part 2'
        solve = solve2(input_str)

    if example:
        print('Solution for example:', solve)
    else:
        submit(day, part, solve, year)


def submit(day: int, part: Literal[1, 2], answer: str | int | None, year: int = YEAR) -> None:
    if not answer:
        print('No answer provided, skipping...')
        return

    verdict_path = f'verdicts/{year}/{day}_{part}.json'
    if os.path.exists(verdict_path):
        with open(verdict_path) as f:
            verdicts = json.load(f)
    else:
        verdicts = []

    print('You are about to submit the follwing answer:')
    print(f'>>>>>>>>>>>>>>>>> {answer}')

    for verdict in verdicts:
        if verdict['answer'] == answer:
            print('Already submitted this answer:', verdict['result'])
            return
        # check for too low/high verdicts
        if verdict['result'] == 'TOO LOW' and answer < verdict['answer']:
            print('Result is too low, skipping...')
            return
        if verdict['result'] == 'TOO HIGH' and answer > verdict['answer']:
            print('Result is too high, skipping...')
            return
        if verdict['result'] == 'OK' and answer != verdict['answer']:
            print(f'Already solved this part with a different answer: {verdict["answer"]}')
            return

    input('Press enter to continue or Ctrl+C to abort.')
    data = {'level': str(part), 'answer': str(answer)}

    response = requests.post(
        f'https://adventofcode.com/{year}/day/{day}/answer', headers={'cookie': 'session=' + AOC_COOKIE}, data=data
    )
    if 'You gave an answer too recently' in response.text:
        # You will get this if you submitted a wrong answer less than 60s ago.
        print('VERDICT : TOO MANY REQUESTS')
    elif 'not the right answer' in response.text:
        if 'too low' in response.text:
            print('VERDICT : WRONG (TOO LOW)')
            verdicts.append({'answer': answer, 'result': 'TOO LOW'})
        elif 'too high' in response.text:
            print('VERDICT : WRONG (TOO HIGH)')
            verdicts.append({'answer': answer, 'result': 'TOO HIGH'})
        else:
            print('VERDICT : WRONG (UNKNOWN)')
            verdicts.append({'answer': answer, 'result': 'UNKNOWN'})
    elif 'seem to be solving the right level.' in response.text:
        # You will get this if you submit on a level you already solved.
        # Usually happens when you forget to switch from `PART = 1` to `PART = 2`
        print('VERDICT : ALREADY SOLVED')
    else:
        print('VERDICT : OK !')
        verdicts.append({'answer': answer, 'result': 'OK'})
        if part == 1:
            with open(f'{day}.1.py', 'r') as in_file, open(f'{day}.2.py', 'w') as out_file:
                out_file.write(in_file.read().replace('solve1', 'solve2').replace('part=1', 'part=2'))
            open_file_in_editor(f'{day}.2.py')
            open_day_in_browser(day, year)

    os.makedirs(os.path.dirname(verdict_path), exist_ok=True)
    with open(verdict_path, 'w') as f:
        json.dump(verdicts, f, indent=2)


if __name__ == '__main__':
    # Example usage

    input_str = get_input(1)
    example_input = get_example(1)
    ans: str | int = ...  # type: ignore Solve the problem given the input
    submit(1, 1, ans)
    ans: str | int = ...  # type: ignore Solve the 2. problem given the input
    submit(1, 2, ans)

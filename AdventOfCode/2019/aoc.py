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

from typing import Literal
import requests

AOC_COOKIE = '53616c7465645f5fbcbf2ae2317bce012d724bdcd3c6754b00e9c44dfba076b7a950dd6ecefb720c53187f7a8e47b20b86a75ab5ac2aa102496dd1fb46e33ff5'
YEAR = 2019


def get_input(day: int, year: int = YEAR) -> str:
    req = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', headers={'cookie': 'session=' + AOC_COOKIE})
    return req.text.strip()


def get_example(day: int, offset: int = 0, year: int = YEAR) -> str:
    req = requests.get(f'https://adventofcode.com/{year}/day/{day}', headers={'cookie': 'session=' + AOC_COOKIE})
    return req.text.split('<pre><code>')[offset + 1].split('</code></pre>')[0].strip()


def submit(day: int, part: Literal[1, 2], answer: str | int, year: int = YEAR) -> None:
    print('You are about to submit the follwing answer:')
    print(f'>>>>>>>>>>>>>>>>> {answer}')
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
        elif 'too high' in response.text:
            print('VERDICT : WRONG (TOO HIGH)')
        else:
            print('VERDICT : WRONG (UNKNOWN)')
    elif 'seem to be solving the right level.' in response.text:
        # You will get this if you submit on a level you already solved.
        # Usually happens when you forget to switch from `PART = 1` to `PART = 2`
        print('VERDICT : ALREADY SOLVED')
    else:
        print('VERDICT : OK !')


if __name__ == '__main__':
    # Example usage

    input_str = get_input(1)
    example_input = get_example(1)
    ans: str | int = ...  # type: ignore Solve the problem given the input
    submit(1, 1, ans)
    ans: str | int = ...  # type: ignore Solve the 2. problem given the input
    submit(1, 2, ans)

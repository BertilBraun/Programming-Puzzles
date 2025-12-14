from aoc import *
from util import *


def parse_game(input: str) -> tuple[int, list[list[int]]]:
    game_id, games = input.split(':')
    game_id = int(game_id.split(' ')[1])
    parsed_games = []
    for game in games.split(';'):
        red, green, blue = 0, 0, 0
        for item in game.split(','):
            count, color = item.strip().split(' ')
            if color == 'red':
                red = int(count)
            elif color == 'green':
                green = int(count)
            elif color == 'blue':
                blue = int(count)
        parsed_games.append([red, green, blue])
    return game_id, parsed_games


def solve2(input: str) -> str | int | None:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    games = [parse_game(x) for x in input.splitlines()]

    power = 0
    for _, games in games:
        power += max(game[0] for game in games) * max(game[1] for game in games) * max(game[2] for game in games)
    return power


if __name__ == '__main__':
    aoc(day=2, part=2, solve2=solve2, example=False)

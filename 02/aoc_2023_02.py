#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-02
Purpose: Solves day 02 from advent of code 2023.
"""

from typing import Final
from dataclasses import dataclass
from functools import reduce
from operator import mul


TEST_DATA: Final = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


@dataclass
class Play:
    """Play consists of several draws each consisting of a number of colored cubes."""
    play_data: dict[str, int]

    @staticmethod
    def from_str(play_str: str) -> "Play":
        """Parse play for input str."""
        return Play(
            play_data={play.strip().split(" ", 2)[1]: int(play.strip().split(" ", 2)[0])
                       for play in play_str.strip().split(",")})


@dataclass
class Game:
    """Game has an id and consists odf a varying amoutn of plays."""
    game_id: int
    game_data: list[Play]

    def is_valid(self, valid_play_data: dict[str, int]) -> bool:
        """Check if game is valid against reference set of cubes in bag."""
        for play in self.game_data:
            for color, amount in play.play_data.items():
                if color in valid_play_data and valid_play_data[color] < amount:
                    return False
        return True

    def min_bag_size(self) -> dict[str, int]:
        """Find minium bag content for game."""
        min_bag: dict[str, int] = {}
        for play in self.game_data:
            for color, amount in play.play_data.items():
                if color not in min_bag:
                    min_bag[color] = amount
                else:
                    min_bag[color] = max(amount, min_bag[color])
        return min_bag

    @staticmethod
    def from_str(line: str) -> "Game":
        """Parse game from input line."""
        game_str, game_data_str = line.rstrip().split(":", 2)
        return Game(
            game_id=int(game_str.replace("Game ", "")),
            game_data=[Play.from_str(plays) for plays in game_data_str.split(";")]
            )


# --------------------------------------------------
def load_data(filename: str):
    """Load input from file."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.readlines()


def parse_game(data) -> list[Game]:
    """Parse input into games."""
    return [Game.from_str(line) for line in data]


def part_01(data) -> str:
    """Solves part 01"""
    games = parse_game(data)
    valid_game = {'red': 12, 'green': 13, 'blue': 14}

    return str(
        sum(
            map(lambda x: x.game_id,
                filter(lambda x: x.is_valid(valid_game), games))
           )
        )


def part_02(data) -> str:
    """solves part 02"""
    games = parse_game(data)

    return str(
        sum(
            reduce(mul, game.min_bag_size().values())
            for game in games)
        )


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split("\n")
    assert '8' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA.split("\n")
    assert '2286' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./02/input')
    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

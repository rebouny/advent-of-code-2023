#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-04
Purpose: Solves day 04 from advent of code 2023.
"""

from typing import Final
from dataclasses import dataclass


TEST_DATA: Final = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


@dataclass
class Card:
    """Card has a number, winning numbers and your 'draw'."""
    index: int
    winning: list[int]
    numbers: list[int]

    @staticmethod
    def from_line(line: str) -> "Card":
        """Construct card from input line."""
        card, game = line.split(':', 2)
        index = int(card.split()[1])
        winners_str, numbers_str = game.split('|')
        # do not forget to filter empty lines
        winners = list(map(int, filter(lambda x: x != '', winners_str.strip().split())))
        numbers = list(map(int, filter(lambda x: x != '', numbers_str.strip().split())))

        return Card(index=index, winning=winners, numbers=numbers)

    def worth(self) -> int:
        """Calculates 'worth' of card."""
        amount = len(set(self.winning).intersection(set(self.numbers)))
        if amount == 0:
            return 0
        return pow(2, amount - 1)

    def matchings(self) -> int:
        """Calculate amount of intersections between your draw and winning numbers."""
        return len(set(self.winning).intersection(set(self.numbers)))


# --------------------------------------------------
def load_data(filename: str):
    """Load input data."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def part_01(data) -> str:
    """Solves part 01"""
    return str(sum(Card.from_line(line).worth() for line in data))


def part_02(data) -> str:
    """solves part 02"""

    lookup = {}
    for line in data:
        card = Card.from_line(line)
        lookup[card.index] = card.matchings()

    cards = []

    for card_no, matches in lookup.items():
        count_card = cards.count(card_no)
        cards.append(card_no)

        for _ in range(count_card + 1):
            for index in range(card_no + 1, card_no + 1 + matches):
                cards.append(index)

    return str(len(cards))


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split('\n')
    assert '13' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA.split('\n')
    assert '30' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./04/input')

    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

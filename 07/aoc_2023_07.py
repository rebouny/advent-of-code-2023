#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-07
Purpose: Solves day 07 from advent of code 2023.
"""

from typing import Final
from enum import Enum
from collections import Counter


TEST_DATA: Final = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


RANK: Final[dict[str, int]] = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}


class HandType(Enum):
    """Define your Hand."""
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7


MAPPING: Final[dict[tuple[int, int], HandType]] = {
    (5, 1): HandType.FIVE_OF_KIND,
    (4, 2): HandType.FOUR_OF_KIND,
    (3, 2): HandType.FULL_HOUSE,
    (3, 3): HandType.THREE_OF_KIND,
    (2, 3): HandType.TWO_PAIR,
    (2, 4): HandType.ONE_PAIR,
    (1, 5): HandType.HIGH_CARD
}


JOKER_MAPPING: dict[tuple[HandType, int], HandType] = {
    (HandType.FIVE_OF_KIND, 0): HandType.FIVE_OF_KIND,
    (HandType.FIVE_OF_KIND, 5): HandType.FIVE_OF_KIND,

    (HandType.FOUR_OF_KIND, 0): HandType.FOUR_OF_KIND,
    (HandType.FOUR_OF_KIND, 1): HandType.FIVE_OF_KIND,
    (HandType.FOUR_OF_KIND, 4): HandType.FIVE_OF_KIND,

    (HandType.THREE_OF_KIND, 0): HandType.THREE_OF_KIND,
    (HandType.THREE_OF_KIND, 1): HandType.FOUR_OF_KIND,
    (HandType.THREE_OF_KIND, 3): HandType.FOUR_OF_KIND,

    (HandType.FULL_HOUSE, 0): HandType.FULL_HOUSE,
    (HandType.FULL_HOUSE, 2): HandType.FIVE_OF_KIND,
    (HandType.FULL_HOUSE, 3): HandType.FIVE_OF_KIND,

    (HandType.TWO_PAIR, 0): HandType.TWO_PAIR,
    (HandType.TWO_PAIR, 1): HandType.FULL_HOUSE,
    (HandType.TWO_PAIR, 2): HandType.FOUR_OF_KIND,

    (HandType.ONE_PAIR, 0): HandType.ONE_PAIR,
    (HandType.ONE_PAIR, 1): HandType.THREE_OF_KIND,
    (HandType.ONE_PAIR, 2): HandType.THREE_OF_KIND,

    (HandType.HIGH_CARD, 0): HandType.HIGH_CARD,
    (HandType.HIGH_CARD, 1): HandType.ONE_PAIR
}


class Hand:
    """Represents a set of 5 cards and it's bid."""
    def __init__(self, cards: str, bid: int, use_joker: bool = False) -> None:
        self.cards = cards
        self.bid = bid
        if use_joker:
            self.type = Hand.strength_joker(cards)
        else:
            self.type = Hand.strengh(cards)

    def __lt__(self, other: "Hand"):
        """Compare hands against each other."""
        if self.type == other.type:
            for i in range(5):
                if RANK[self.cards[i]] != RANK[other.cards[i]]:
                    return RANK[self.cards[i]] < RANK[other.cards[i]]
            raise ValueError("illegal")  # Failure state
        return self.type.value < other.type.value

    def __repr__(self) -> str:
        return f"{self.cards}: {self.type.value} / {self.bid}"

    @staticmethod
    def from_line(line: str, use_joker: bool = False) -> "Hand":
        """Initialize from input line."""
        cards, bid = line.split()
        return Hand(cards=cards, bid=int(bid), use_joker=use_joker)

    @staticmethod
    def strengh(cards: str) -> HandType:
        """Determine strength of hand"""
        counter = Counter(cards)
        highest_count = counter.most_common()[0][1]
        sets = len(set(cards))
        return MAPPING[(highest_count, sets)]

    @staticmethod
    def strength_joker(cards: str) -> HandType:
        """Determine strength of hand when using joker."""
        j_count = cards.count("J")
        j_type = Hand.strengh(cards)

        return JOKER_MAPPING[(j_type, j_count)]


# --------------------------------------------------
def load_data(filename: str):
    """Load input from file."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def part_01(data) -> str:
    """Solves part 01."""
    hands = sorted([Hand.from_line(line=line) for line in data])

    return str(
        sum(
            i * hand.bid for i, hand in enumerate(hands, start=1)
        )
    )


def part_02(data) -> str:
    """solves part 02."""
    # we need to pimp 'J's score, yes, that's really direty
    RANK['J'] = 1
    hands = sorted([Hand.from_line(line=line, use_joker=True) for line in data])

    return str(
        sum(
            i * hand.bid for i, hand in enumerate(hands, start=1)
        )
    )


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split('\n')
    assert '6440' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA.split('\n')
    assert '5905' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./07/input')
    # data = TEST_DATA.split('\n')
    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-01
Purpose: Solves day 01 from advent of code 2023.
"""

from typing import Final


NUMBERS: Final[list[str]] = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

NUMBERS_DIGITS: Final[list[str]] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


TEST_DATA: Final[str] = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


TEST_DATA_2: Final[str] = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def load_data(filename: str):
    """Load inpit file."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return file.readlines()


def part_01(data) -> str:
    """Solves part 01"""
    return str(
        sum(
            build_number(
                list(filter(lambda x: x.isdigit(), line.rstrip()))
            ) for line in data
        )
    )


def replace_first_and_last(data: str) -> str:
    """Recursion step to replace next number by digit."""
    idx: tuple[int, int] = (-1, -1)

    for i, number in enumerate(NUMBERS, start=0):
        idx_n = data.find(number)
        if idx_n > -1 and (idx == (-1, -1) or idx_n < idx[0]):
            idx = (idx_n, i)
    for i, number in enumerate(NUMBERS_DIGITS, start=0):
        idx_n = data.find(number)
        if idx_n > -1 and (idx == (-1, -1) or idx_n < idx[0]):
            idx = (idx_n, i)

    if idx == (-1, -1):
        return data
    data = data.replace(NUMBERS[idx[1]], str(idx[1] + 1))
    idx = (-1, -1)

    for i, number in enumerate(NUMBERS, start=0):
        idx_n = data.rfind(number)
        if idx_n > -1 and (idx == (-1, -1) or idx_n > idx[0]):
            idx = (idx_n, i)
    for i, number in enumerate(NUMBERS_DIGITS, start=0):
        idx_n = data.rfind(number)
        if idx_n > -1 and (idx == (-1, -1) or idx_n > idx[0]):
            idx = (idx_n, i)

    if idx != (-1, -1):
        data = data.replace(NUMBERS[idx[1]], str(idx[1] + 1))

    return data


def build_number(numbers: list[int]) -> int:
    """Pick first and last digit from list and combine into number."""
    return int(f"{numbers[0]}{numbers[-1]}")


def part_02(data) -> str:
    """solves part 02"""
    return str(
        sum(
            build_number(
                list(filter(lambda x: x.isdigit(),
                            replace_first_and_last(line.rstrip())))
            ) for line in data
        )
    )


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split()
    assert "142" == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA_2.split()
    assert '281' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./01/input')
    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

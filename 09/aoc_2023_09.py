#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-09
Purpose: Solves day 09 from advent of code 2023.
"""

from typing import Final


TEST_DATA: Final = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


# --------------------------------------------------
def load_data(filename: str):
    """Load input lines."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def extrapolate(values: list[int]) -> int:
    """Extrapolate list of values."""
    historic: list[int] = [values[-1]]

    while any(values):
        values = [values[i + 1] - values[i] for i in range(len(values) - 1)]
        historic.append(values[-1])

    return sum(historic)


def extrapolate_backwards(values: list[int]) -> int:
    """Extrapolate list of values."""
    historic: list[int] = [values[0]]

    while any(values):
        values = [values[i + 1] - values[i] for i in range(len(values) - 1)]
        historic.append(values[0])

    ext = 0
    for i in range(len(historic), 0, -1):
        ext = historic[i - 1] - ext

    return ext


def part_01(data) -> str:
    """Solves part 01"""
    return str(
        sum(
            (  # generator
                extrapolate(
                    list(
                        map(int, line.split())
                    )
                ) for line in data
            )
        )
    )


def part_02(data) -> str:
    """solves part 02"""
    return str(
        sum(
            (  # generator
                extrapolate_backwards(
                    list(
                        map(int, line.split())
                    )
                ) for line in data
            )
        )
    )


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split('\n')
    assert '114' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA.split('\n')
    assert '2' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./09/input')
    # data = TEST_DATA.split('\n')
    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

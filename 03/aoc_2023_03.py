#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-03
Purpose: Solves day 03 from advent of code 2023.
"""

from typing import Final, Optional
from functools import reduce
from operator import mul
import re


TEST_DATA: Final = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


REGEX_NUMBER: Final[re.Pattern] = re.compile(r'\d+')


# --------------------------------------------------
def load_data(filename: str):
    """Load input data."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def surrounds(j: int, i: int, finding: str, width: int, signs: list[tuple[int, int]]) -> bool:
    """Check if finding at given coordinate 'touches' a sign given by list."""
    for y in range(j-1, j+2):
        for x in range(i-1, i+len(finding)+1):
            if y < 0 or x < 0 or x == width:  # skip out of bounds
                continue
            if y == j and x in range(i, i + len(finding)):  # skip finding digits
                continue
            if (y, x) in signs:
                return True
    return False


def get_signs(data, restrict: Optional[str] = None) -> list[tuple[int, int]]:
    """Find 'sign' elements in input data, optionally restrict to certain sign."""
    signs = []

    for j, line in enumerate(data):
        for i, char in enumerate(line):
            if restrict:
                if restrict == char:
                    signs.append((j, i))
            elif char not in ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                signs.append((j, i))

    return signs


def part_01(data) -> str:
    """Solves part 01"""
    width = len(data[0])
    schematic = 0
    signs = get_signs(data)

    for j, line in enumerate(data):
        for finding in REGEX_NUMBER.finditer(line):
            if surrounds(j, finding.start(), finding.group(), width, signs):
                schematic += int(finding.group())

    return str(schematic)


def part_02(data) -> str:
    """solves part 02"""
    signs = get_signs(data, '*')
    width = len(data[0])
    findings = []

    for j, line in enumerate(data):
        for finding in REGEX_NUMBER.finditer(line):
            if surrounds(j, finding.start(), finding.group(), width, signs):
                findings.append((j, finding.start(), finding.group()))

    gear_ratios = 0
    for sign in signs:
        adj = list(filter(lambda x: surrounds(x[0], x[1], x[2], width, [sign]), findings))
        if len(adj) == 2:
            gear_ratios += reduce(mul, map(lambda x: int(x[2]), adj))

    return str(gear_ratios)


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split('\n')
    assert '4361' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA.split('\n')
    assert '467835' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./03/input')

    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

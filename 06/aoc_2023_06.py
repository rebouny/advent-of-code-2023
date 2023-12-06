#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-06
Purpose: Solves day 06 from advent of code 2023.
"""

from typing import Final
from dataclasses import dataclass
from functools import reduce
from operator import mul
import math


TEST_DATA: Final = """Time:      7  15   30
Distance:  9  40  200"""


@dataclass
class Race:
    """Contains a race."""
    time: int
    duration: int


def solve(time: int, distance: int) -> tuple[float, float]:
    """Solve quadtratic equation."""
    result_add = time / 2.0 + math.sqrt(pow(time/2.0, 2) - distance)
    result_sub = time / 2.0 - math.sqrt(pow(time/2.0, 2) - distance)

    return result_add, result_sub


# --------------------------------------------------
def load_data(filename: str):
    """Load data from input."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def parse_input(data: list[str]) -> list[Race]:
    """Parse races out of input."""
    times = map(int, data[0].split(':')[1].strip().split())
    durations = map(int, data[1].split(':')[1].strip().split())

    return [Race(time=x[0], duration=x[1]) for x in zip(times, durations)]


def interval(boundaries: tuple[float, float]) -> int:
    """Trunc race time intersections to valid interval length."""
    return len(
        range(
            math.floor(boundaries[1] + 1),
            # we really need to be careful with upper boundary, we need to beat (gt) race distance
            math.floor(boundaries[0] if boundaries[0].is_integer() else boundaries[0] + 1)
        )
    )


def part_01(data) -> str:
    """Solves part 01"""
    races = parse_input(data)

    return str(
        reduce(mul, [interval(solve(race.time, race.duration)) for race in races])
    )


def part_02(data) -> str:
    """solves part 02"""
    races = parse_input(data)

    # fix wrongly parsed race input
    time = int("".join(map(str, map(lambda x: x.time, races))))
    duration = int("".join(map(str, map(lambda x: x.duration, races))))

    return str(
        interval(solve(time, duration))
    )


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split('\n')
    assert '288' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA.split('\n')
    assert '71503' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./06/input')
    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

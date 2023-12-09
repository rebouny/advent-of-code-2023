#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-05
Purpose: Solves day 05 from advent of code 2023.
"""

from typing import Final, Optional
from dataclasses import dataclass
from tqdm import tqdm as tq


TEST_DATA: Final = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


@dataclass
class Entry:
    """Entry parsed from input."""
    destination_start: int
    source_start: int
    range_length: int

    @staticmethod
    def from_line(line: str) -> "Entry":
        """Initializes entry from input line."""
        dst_start, src_start, length = list(map(int, line.split()))
        return Entry(destination_start=dst_start,
                     source_start=src_start,
                     range_length=length)


@dataclass
class Map:
    """Define a mapping step."""
    map: list[Entry]

    def convert(self, number: int) -> int:
        """Check if number is in range, copy otherwise."""
        for entry in self.map:
            if entry.source_start <= number < (entry.source_start + entry.range_length):
                return number - entry.source_start + entry.destination_start
        return number


# --------------------------------------------------
def load_data(filename: str):
    """Load lines from input."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def chunks(data: list[int], chunk_size: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def convert(number: int, maps: list[Map]) -> int:
    """Push number through conversion chain."""
    for item in maps:
        number = item.convert(number)
    return number


def parse_input(data):
    """Parse maps from data."""
    _, items = data[0].split(":")
    seeds: list[int] = list(map(int, items.strip().split()))

    maps: list[Map] = []

    # start = 3
    start = 0
    end = 1

    for i in range(7):
        start += end + 2
        if i != 6:  # ignore end calculation on last entry
            end = (data[start:]).index("")
        maps.append(Map(map=[Entry.from_line(line) for line in data[start:start+end]]))

    return seeds, maps


def part_01(data) -> str:
    """Solves part 01"""
    seeds, maps = parse_input(data)

    return str(
        min(
            (  # generator
                convert(seed, maps) for seed in tq(seeds, total=len(seeds))
            )
        )
    )


def part_02(data) -> str:
    """solves part 02"""
    seeds, maps = parse_input(data)

    seed_pairs = chunks(seeds, 2)

    lowest: Optional[int] = None

    for pair in tq(seed_pairs, total=(len(seeds) / 2), position=0):
        idx = pair[0]
        with tq(total=pair[1], position=1, leave=False) as inner_bar:
            while idx < pair[0] + pair[1]:
                result = convert(idx, maps)
                if lowest:
                    lowest = min(lowest, result)
                else:
                    lowest = result
                idx += 1
                inner_bar.update(1)

    return str(lowest)


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split('\n')
    assert '35' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = TEST_DATA.split('\n')
    assert '46' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    # data = load_data('./05/input')
    data = TEST_DATA.split('\n')
    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

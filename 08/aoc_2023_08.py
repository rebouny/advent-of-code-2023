#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Martin Schuh <development@rebouny.net>
Date   : 2023-12-08
Purpose: Solves day 08 from advent of code 2023.
"""

from typing import Final, Any, Generator
from functools import reduce
import re


LINE_REGEX: Final[re.Pattern] = re.compile(r'^([0-9A-Z]{3})\ =\ \(([0-9A-Z]{3}),\ ([0-9A-Z]{3})\)$')

TEST_DATA: Final = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""


ANOTHER_TEST_DATA: Final = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


STAGE_TWO_TEST_DATA: Final[str] = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


MAP_INST_TO_IDX: Final[dict[str, int]] = {
    'L': 0,
    'R': 1
}

# https://www.grund-wissen.de/informatik/python/scipy/mathematik-mit-standard-modulen.html


def greated_common_divisor(a: int, b: int) -> int:
    """Return the greatest common divisor using Euclid's Algorithm."""
    while b:
        a, b = b, a % b
    return a


def lowest_common_multiplier(a: int, b: int) -> int:
    """Return lowest common multiple."""
    return int(a * b / greated_common_divisor(a, b))


def lowest_common_multiplier_many(args: list[int]) -> int:
    """Turn lcm of args."""
    return reduce(lowest_common_multiplier, args)


# --------------------------------------------------
def load_data(filename: str):
    """Load lines from input data."""
    with open(filename, 'rt', encoding='utf-8') as file:
        return [line.rstrip() for line in file.readlines()]


def parse_nodes(data: list[str]) -> dict[str, tuple[str, str]]:
    """Parse routing nodes into map by using regex.

    As input is hard wired we've could used string indexing as well."""
    nodes: dict[str, tuple[str, str]] = {}

    for line in data:
        match = LINE_REGEX.match(line)
        if not match:
            raise ValueError("parsing error")
        nodes[match.group(1)] = (match.group(2), match.group(3))
    return nodes


def instruction_generator(instructions: str) -> Generator[str, Any, None]:
    """Generate endlessly path traversal instructions."""
    while True:
        for instruction in instructions:
            yield instruction


def part_01(data) -> str:
    """Solves part 01"""
    instructions = data[0]

    nodes = parse_nodes(data[2:])
    key = 'AAA'

    for count, instruction in enumerate(instruction_generator(instructions), start=1):
        value = nodes[key][MAP_INST_TO_IDX[instruction]]
        if value == 'ZZZ':
            return str(count)
        key = value

    return ''  # just to get rid of pylints W0631


def find_path_length(key: str, instructions: str, nodes: dict[str, tuple[str, str]]) -> int:
    """Find path length for given key by traversing along instructions."""
    for count, instruction in enumerate(instruction_generator(instructions), start=1):
        value = nodes[key][MAP_INST_TO_IDX[instruction]]
        if value[2] == 'Z':
            return count
        key = value
    return 0  # just to get rid of pylints R1710


def part_02(data) -> str:
    """Solves part 2.

    After doing some tests I noticed that each possible start value has only one
    terminating value in it's path, so the problem reduces in finding the lowest
    common multiplyer.
    """
    instructions = data[0]
    nodes = parse_nodes(data[2:])
    node_keys = [key for key in nodes if key[2] == 'A']

    path_lengths = [find_path_length(key, instructions, nodes) for key in node_keys]

    return str(lowest_common_multiplier_many(path_lengths))


# def part_02(data) -> str:
#     """solves part 02"""

#     # brute force, this never ends
#     instructions = data[0]

#     nodes = parse_nodes(data[2:])
#     node_keys = [key for key in nodes if key[2] == 'A']

#     for count, instruction in enumerate(instruction_generator(instructions), start=1):
#         values = [nodes[key][MAP_INST_TO_IDX[instruction]] for key in node_keys]

#         if all(list(map(lambda x: x[2] == 'Z', values))):
#             break

#         node_keys = values

#     return str(count)


# --------------------------------------------------
def test_part_01():
    """Tests part 01"""
    data = TEST_DATA.split('\n')
    assert '2' == part_01(data)


def test_part_02():
    """Tests part 02"""
    data = STAGE_TWO_TEST_DATA.split('\n')
    assert '6' == part_02(data)


# --------------------------------------------------
def main() -> None:
    """Main wrapper."""
    data = load_data('./08/input')
    # data = TEST_DATA.split('\n')
    # data = ANOTHER_TEST_DATA.split('\n')
    # data = STAGE_TWO_TEST_DATA.split('\n')
    print(part_01(data))
    print(part_02(data))


if __name__ == '__main__':
    main()

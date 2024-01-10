import re
from abc import ABC
from collections.abc import Iterator
from math import prod

from aoc.problems import MultiLineProblem
from aoc.utils import group_tuples


class _Problem(MultiLineProblem[int], ABC):
    def parsed(self) -> Iterator[dict[str, int]]:
        for line in self.lines:
            yield {k: max(v) for k, v in group_tuples(
                (c, int(a)) for a, c in re.findall(r'(\d+) (\w)', line)
            ).items()}


class Problem1(_Problem):
    test_solution = 8
    my_solution = 2600

    def solution(self) -> int:
        return sum(i for i, d in enumerate(self.parsed(), 1) if (
            d['r'] <= 12 and d['g'] <= 13 and d['b'] <= 14
        ))


class Problem2(_Problem):
    test_solution = 2286
    my_solution = 86036

    def solution(self) -> int:
        return sum(prod(d.values()) for d in self.parsed())


TEST_INPUT = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

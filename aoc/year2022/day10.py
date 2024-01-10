from abc import ABC
from collections.abc import Iterator
from itertools import batched
from typing import Generic, TypeVar

from aoc.problems import MultiLineProblem
from aoc.utils import try_convert

T = TypeVar('T')


class _Problem(MultiLineProblem[T], ABC, Generic[T]):
    def moves(self) -> Iterator[int]:
        x = 1
        for line in self.lines:
            for s in line.split():
                yield x
                x += try_convert(int, s, 0)


class Problem1(_Problem[int]):
    test_solution = 13140
    my_solution = 13180

    def solution(self) -> int:
        return sum(
            cycle * x
            for cycle, x in enumerate(self.moves(), 1)
            if (cycle + 20) % 40 == 0
        )


class Problem2(_Problem[str]):
    test_solution = """
██░░██░░██░░██░░██░░██░░██░░██░░██░░██░░
███░░░███░░░███░░░███░░░███░░░███░░░███░
████░░░░████░░░░████░░░░████░░░░████░░░░
█████░░░░░█████░░░░░█████░░░░░█████░░░░░
██████░░░░░░██████░░░░░░██████░░░░░░████
███████░░░░░░░███████░░░░░░░███████░░░░░
"""

    my_solution = """
████░████░████░░██░░█░░█░░░██░░██░░███░░
█░░░░░░░█░█░░░░█░░█░█░░█░░░░█░█░░█░█░░█░
███░░░░█░░███░░█░░░░████░░░░█░█░░█░███░░
█░░░░░█░░░█░░░░█░░░░█░░█░░░░█░████░█░░█░
█░░░░█░░░░█░░░░█░░█░█░░█░█░░█░█░░█░█░░█░
████░████░█░░░░░██░░█░░█░░██░░█░░█░███░░
"""

    def solution(self) -> str:
        return '\n'.join(''.join(
            '█' if p - 1 <= i <= p + 1 else '░'
            for i, p in enumerate(sprite_positions)
        ) for sprite_positions in batched(self.moves(), 40))


TEST_INPUT = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

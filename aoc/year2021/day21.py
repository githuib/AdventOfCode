from abc import ABC
from functools import cache
from itertools import product

from aoc.problems import ParsedProblem
from aoc.utils import mods


def update_score(pos: int, score: int, roll: int) -> tuple[int, int]:
    return (pos := mods(pos + roll, 10, 1)), score + pos


def move_pawn(
    p1: int, p2: int, s1: int, s2: int,
    is_turn1: bool, roll: int,
) -> tuple[int, int, int, int, bool]:
    if is_turn1:
        p1, s1 = update_score(p1, s1, roll)
    else:
        p2, s2 = update_score(p2, s2, roll)
    return p1, p2, s1, s2, not is_turn1


def turn(
    p1: int, p2: int, s1: int = 0, s2: int = 0,
    is_turn1: bool = True, total_rolls: int = 0,
) -> tuple[int, int, int]:
    if s1 >= 1000 or s2 >= 1000:
        return s1, s2, total_rolls
    return turn(*move_pawn(
        p1, p2, s1, s2, is_turn1,
        roll=sum(mods(total_rolls + die, 100, 1) for die in range(1, 4)),
    ), total_rolls + 3)


@cache
def quantum_turn(
    p1: int, p2: int, s1: int = 0, s2: int = 0,
    is_turn1: bool = True,
) -> list[int]:
    if s1 >= 21:
        return [1, 0]
    if s2 >= 21:
        return [0, 1]
    return [sum(games_won) for games_won in zip(*[
        quantum_turn(*move_pawn(p1, p2, s1, s2, is_turn1, sum(rolls)))
        for rolls in product(range(1, 4), repeat=3)
    ])]


class _Problem(ParsedProblem[tuple[int], int], ABC):
    line_pattern = 'position: {:d}'

    def __init__(self):
        [self.start_1], [self.start_2] = self.parsed_input


class Problem1(_Problem):
    test_solution = 739785
    my_solution = 432450

    def solution(self) -> int:
        *scores, rolls = turn(self.start_1, self.start_2)
        return min(scores) * rolls


class Problem2(_Problem):
    test_solution = 444356092776315
    my_solution = 138508043837521

    def solution(self) -> int:
        return max(quantum_turn(self.start_1, self.start_2))


TEST_INPUT = """
Player 1 starting position: 4
Player 2 starting position: 8
"""

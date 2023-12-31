from enum import IntEnum
from itertools import batched

from aoc.problems import NoSolutionFound
from aoc.utils import compare
from aoc.year2019.intcode import IntcodeProblem


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


class Problem1(IntcodeProblem[int]):
    test_solution = None
    my_solution = 333

    def solution(self) -> int:
        return list(self.computer.run_to_next_output())[2::3].count(Tile.BLOCK)


class Problem2(Problem1):
    test_solution = None
    my_solution = 16539

    def solution(self) -> int:
        self.computer.program[0] = 2
        score, paddle_x = None, None
        for x, y, value in batched(self.computer.run_to_next_output(), 3):
            if (x, y) == (-1, 0):
                score = value
            elif value == Tile.PADDLE:
                paddle_x = x
            elif value == Tile.BALL:
                direction = 0 if paddle_x is None else compare(paddle_x, x)
                self.computer.inputs.append(direction)
        if score:
            return score
        raise NoSolutionFound


TEST_INPUT = """

"""

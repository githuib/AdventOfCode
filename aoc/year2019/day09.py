from abc import ABC

from aoc.year2019.intcode import IntcodeProblem


class _Problem(IntcodeProblem[int], ABC):
    n: int

    def solution(self) -> int:
        return self.computer.run(self.n)


class Problem1(_Problem):
    test_solution = None
    my_solution = 2406950601

    n = 1


class Problem2(_Problem):
    test_solution = None
    my_solution = 83239

    n = 2


TEST_INPUT = """

"""

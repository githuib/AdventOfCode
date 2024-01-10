import logging
from abc import ABC
from typing import Iterable, NamedTuple, Self

from more_itertools import last

from aoc import AOC, InputMode
from aoc.geo2d import P2, Mat2
from aoc.problems import FatalError, GridProblem, var
from aoc.search import BFSState
from aoc.utils import repeat_transform


class Constants(NamedTuple):
    grid: Mat2[str]
    steps: int


class Variables(NamedTuple):
    pos: P2
    count_me: bool


class GardenState(BFSState[Constants, Variables]):
    @property
    def is_finished(self) -> bool:
        return self.cost > self.c.steps

    @property
    def next_states(self: Self) -> Iterable[Self]:
        for p, v in self.c.grid.neighbors(self.v.pos):
            if v != '#':
                yield self.move(pos=p, count_me=not self.v.count_me)


class _Problem(GridProblem[int], ABC):
    def __init__(self):
        self.start = self.grid.point_with_value('S')

    def num_garden_plots_slow_af(self, steps: int) -> int:
        def step(points: set[P2]) -> set[P2]:
            return {n for p in points for n, v in self.grid.neighbors(p) if v != '#'}
        return len(last(repeat_transform({self.start}, step, times=steps)))

    def num_garden_plots(self, steps: int) -> int:
        path = GardenState.find_path(Variables(self.start, steps % 2 == 0), Constants(self.grid, steps))
        return sum(s.v.count_me for s in path.visited)


class Problem1(_Problem):
    test_solution = 16
    my_solution = 3591

    def solution(self) -> int:
        return self.num_garden_plots(var(test=6, puzzle=64))


class Problem2(_Problem):
    test_solution = None
    my_solution = 598044246091826

    def infinite_plots(self, steps: int) -> int:
        if AOC.input_mode == InputMode.TEST:
            raise FatalError('This approach only works for the puzzle data!')
        size, (center, _) = self.grid.width, self.start
        c, u1, u2 = [self.num_garden_plots(center + size * i) for i in range(3)]
        b = (u1 * 4 - u2 - c * 3) / 2
        a = u1 - b - c
        n = (steps - center) / size
        return round(n ** 2 * a + n * b + c)

    def solution(self) -> int:
        self.grid.infinite = True
        if AOC.input_mode == InputMode.TEST:
            for i, s in [(6, 16), (10, 50), (50, 1594), (100, 6536), (500, 167004), (1000, 668697)]:  # (5000, 16733044)
                ans = self.num_garden_plots(i)
                logging.info('Checking input %d: %s == %s -> %s', i, s, ans, '👌' if ans == s else 'Nope')
            return 0
        return self.infinite_plots(26501365)


TEST_INPUT = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

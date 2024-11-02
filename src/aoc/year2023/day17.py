from abc import ABC
from collections.abc import Iterator
from typing import NamedTuple, Self

from aoc.geo2d import P2, Dir2, Grid2, Range
from aoc.problems import NumberGridProblem
from aoc.search import DijkstraState


class Constants:
    def __init__(self, map_: Grid2, segment_range: Range):
        self.map = map_
        self.min_segment, self.max_segment = segment_range
        self.end = map_.width - 1, map_.height - 1


class Variables(NamedTuple):
    pos: P2 = 0, 0
    from_dir: P2 | None = None
    seg_length: int = 0


DIRS: dict[P2 | None, list[P2]] = {
    Dir2.left: [Dir2.left, Dir2.up, Dir2.down],
    Dir2.right: [Dir2.right, Dir2.up, Dir2.down],
    Dir2.up: [Dir2.up, Dir2.left, Dir2.right],
    Dir2.down: [Dir2.down, Dir2.left, Dir2.right],
    None: Dir2.direct_neighbors,
}


class LavaState(DijkstraState[Constants, Variables]):
    @property
    def is_finished(self) -> bool:
        return self.v.pos == self.c.end and not 0 < self.v.seg_length < self.c.min_segment

    @property
    def next_states(self: Self) -> Iterator[Self]:
        x, y = self.v.pos
        for dx, dy in DIRS[self.v.from_dir]:
            p = (x + dx, y + dy)
            same_dir = (dx, dy) == self.v.from_dir
            new_seg_length = self.v.seg_length + 1 if same_dir else 1
            if (
                p in self.c.map
            ) and (
                new_seg_length <= self.c.max_segment
            ) and (
                same_dir or not 0 < self.v.seg_length < self.c.min_segment
            ):
                yield self.move(pos=p, from_dir=(dx, dy), seg_length=new_seg_length, distance=self.c.map[p])


class _Problem(NumberGridProblem[int], ABC):
    segment_range: Range

    def solution(self) -> int:
        return LavaState.find_path(Variables(), Constants(self.grid, self.segment_range)).length


class Problem1(_Problem):
    test_solution = 102
    my_solution = 953

    segment_range = 0, 3


class Problem2(_Problem):
    test_solution = 94
    my_solution = 1180

    segment_range = 4, 10


TEST_INPUT = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

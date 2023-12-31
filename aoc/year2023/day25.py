from math import prod

from igraph import Graph  # type: ignore[import-untyped]

from aoc.problems import MultiLineProblem


class Problem1(MultiLineProblem[int]):
    test_solution = 54
    my_solution = 582590

    def solution(self) -> int:
        return prod(len(c) for c in Graph.ListDict(
            {line[:3]: line[5:].split() for line in self.lines}
        ).mincut().partition)


TEST_INPUT = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

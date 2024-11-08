from abc import ABC
from collections.abc import Iterator

from aoc.geo2d import P2, Dir2, grid_area, loop_length
from aoc.problems import GridProblem, NoSolutionFoundError

CONNECTIONS = {
    "S": Dir2.direct_neighbors,
    ".": (),
    "|": (Dir2.up, Dir2.down),
    "-": (Dir2.left, Dir2.right),
    "L": (Dir2.up, Dir2.right),
    "J": (Dir2.left, Dir2.up),
    "7": (Dir2.left, Dir2.down),
    "F": (Dir2.down, Dir2.right),
}


class _Problem(GridProblem[int], ABC):
    def first_neighbor(self, sx: int, sy: int) -> P2:
        for (x, y), v in self.grid.neighbors((sx, sy)):
            if v != "." and (sx - x, sy - y) in CONNECTIONS[v]:
                return x, y
        raise NoSolutionFoundError

    def vertices(self) -> Iterator[P2]:
        sx, sy = self.grid.point_with_value("S")
        x, y = self.first_neighbor(sx, sy)
        yield x, y
        while (v := self.grid[x, y]) not in ".S":
            if (from_dir := (sx - x, sy - y)) in (conn := CONNECTIONS[v]):
                if v in "LJ7F":
                    yield x, y
                dx, dy = conn[1 - conn.index(from_dir)]
                sx, sy, x, y = x, y, x + dx, y + dy


class Problem1(_Problem):
    test_solution = 80
    my_solution = 7107

    def solution(self) -> int:
        return loop_length(self.vertices()) // 2


class Problem2(_Problem):
    test_solution = 10
    my_solution = 281

    def solution(self) -> int:
        return grid_area(self.vertices(), include_loop=False)


# FANCY_TILES = dict(zip('S.|-LJ7F', '╬.║═╚╝╗╔'))
# def logging.debug_grid(self, outside: set[P2] = None) -> None:
#     def color(v: int | None, o: bool) -> str:
#         v = v or 1
#         match v, o:
#             case 0, _:
#                 return chalk.hex('333').bg_hex('f08')(FANCY_TILES[v])  # start
#             case v, _ if 0 < v <= 7:
#                 return chalk.hex('058' if o else '999').bg_hex('0af' if o else '641')(FANCY_TILES[v])  # crap
#             case v, False if v < 0:
#                 return chalk.hex('333').bg_hex('eca')(FANCY_TILES[-v])  # loop
#             case _:
#                 return '?'  # should never happen
#
#     logging.debug(' ')
#     logging.debug(lambda: self.grid.to_str(lambda p, v: color(v, p in outside if outside else False)))


# TEST_INPUT = """
# ..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ...
# """

TEST_INPUT = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

# TEST_INPUT = """
# JF|7F.L-J7|||FFJ.-.7L-||JL.J7F.F-77JLJ-L-|JFF7F|LL.777-F7LF-F|F7LL.7-JFJJ7...F|-|LL||-LL7FLFL-|L7.J-.F7-||J-J-F7|JJ-L.FFJ|F|FLF--|L.--J.-L|7--|..FF-JLJ..L|J-|.J7FJFF|L..|7L-|L|--F7J.L.-|7JLF7J-.|-..L7.-.F7JJFF||LLL77FJFF-JJ7|J7-.-J7J|.-F77|FJL.|L-LJJLL.|J|J-|L-.L-7L-JJ-L-7.L7LLF.F.J.-7JF-FL7.|LJ-7L|.-77L-||..L|J|F7|.7LJ7|.|LLJ-LFLF.JL7L7J--.7..-LF77L...--FJFF7LJ..|.L.JF-7.JL7.JFF-JFF7LJJ7..J.-LJ7FL-LLJF.7FJ-|JL.-
# JLL7-|-F|.-LFL|7J-|.---.J|F-J.J|.F-L-LLJ.777.L7L7..77FFJ.||.|-JLJJ|77|-|FL-J.7FJ.JFJ7|-J-JJJ7FFL7-7FJ77.|L-JL-JLF7FL-F-LLF|FJ.FJL||JLFLF-77JL.|7--.7LF.-.LJJLJ-...-|.-JJL||LJF.7-.LL-7L|.J.-.|J|FL--LF.FJL-7J||F--7F----7L-FJ---LFJ|JJ|-7-F|LL-.J|J.F7L7..|..7.L.LL.7J|F.-.LF.-FJFJ.F.F.|-|.7JL.F-.JFL|-L..7F77|.JL.|.L||JF.7|J.F-.|LF|--F|-.7.J7FLL-LFF.77L-7.7JJJ|77JL||LF|7.LJ..|FLJ.7LLJ.F|L-.J7-7L.JL-|L.L7F|F-L||.|-JJ7-77
# J|7-|7FFJ7LLFFF|J-F.FFF7LLF-LJJJ7F7JL-.J-J...7|LF..7F.J|-F7.||JJ.-|-.-L|LL-.JLL-7F|FJ|JJF.7.L--|||F|FLJJL|JFJLJL..L|F.J.7JL|LFJ|-7JL7|-JJF-7-L-.-F.L-|.J|-.|7-.-L|LJ.J|L--..|LL-LL--.--|LJJ7|J7.|JL|||LL7.F.|J||F-JL-7F-J.-LJ-|7L|L-77JJLL.7F-J.777-|.F|L--JF|.JLF||FF7J|L7J7-7JF7F|J7J-.LJ-FJ7LF|-.-.|.F7-7F-...LL|77F.-J-J..7|-J|FJF|7LJ-.FJ-F77F7F7.--F-.|-|JL-FL.-FLF.LFL..|J|7F.||-F-.FJ-J|JF7F|J-.FJL7.7LL.FF--||J|-|.F---
# 77LJ||-7-.J7J-.-|LLF7.7J.LL7-.F-7J7-F7-||FL.JL7-F7-J77..7L-.-F.J.|-7|77F|JJFJJJLJL7L.FLLF.L.-.|-7FL||-LF-|LLL-7||7-F|||7F.J7JFJ7F77-|LL7|J7J7|7J7.L7-L.J|7LJ.J.F||FJ.|F7LLJ.||LL777LFL|JFL.JLL|.J|FL|--.7F77JF-JL----J||7JLFLF|F||-|-7--L.F7-F7F7.77J7--|-7FL.J.FJ..-L7F..7FL|7|F|7L.F|LJL77F.7FF-FF||7L.FL-|J7F.7F|-.JJ.F|L||.-F-|.||FJ.FFF7FFFLF||J.L.-LJ|-.J|.F.JF|.FL.L|J7.--LL7L7.L-|F77||J7LJJLL.-|JL..L7J|L7-.|JLL|7L.FJ-
# L7L|LLL-L.-FF|.-JJ|.-LJJFJJF7|-FFJ-|7|-.7F|F|J|.7|LLF7.||JLF7FJJ-|.-L.77|F-|FFJJLL|L|F.FF7.|.|FF7.LF7-J7J.-|7FJ.7FL.-7..7LF-F7F..|L|-..LF77J7FJ.FF---JJLFLL.F-7FFJJ-7-J7|F-7FJJ|7LJ-7-J.|FF||-FL7|-||.7|F|..-L-7F--7F7|.|-..JJ-|J.--J|LFFF7||F.7--7JJ7.L|JJLJL|-FF|F-...|--7J-F7-.7JJJ7L7L|.J7JJL|-L-.7.J-J|J|LJ-7.--||.JL--F.|-.JL-J|.77|F.JFF|F|--7||F.-7|.--|77|.77FF7FF.F7J77..LJLLL-L.F|-FLLL-J-L-LJ.||FJJJ|.--.-|..F.|JL|-
# -FLLJFF|7-|7LF------------77L7..J7|.|.-FLF..FF-F----7F------7J-FLJ.LJF.L-L|..|J-L.-.LLFJ-LJ.FLJ.J|J.7-7LL-..L7-J|F---JJ7L||F7|L-JFJ77L.--JFF||L7F77-FJJ7F.JFFJ-J|JF|..7J-|7L.FFF.J.|JF----------7F7F----7J|.-|.||F-J||||-7.-FF....7-|-|FFLF7|LJ.F-7LJ|J|LL|F-7||F|LF-|7|-7.JL.L77L|L7|...7L|J77-|.J.--|F-LL7JFFFF--7||-.J7---J7-J7F|LF7-L|LL7.|.-..L|LLJLJ|..7J7F|...J||7|FJJ7FLF.F|FF-777J-|..|L-.FL7J-.-.FL.FJF|LL|JJF7F--7|J.
# -.L-F|LJJL|LJL---7F7F----7||JLJ.-.F77-7-LFF7FL|L---7||F7F---J|F.-F77F..|7||LLFL--7FJ..J|F7-77FF.J7|LLJF|J.LJ.L|J.--FFJ-J7F.7F7|7---FF|F.7F7LJ7L7J7J-|LL77F.L-|.7|F.|.F-J|7FF7J-L|7LF7|F7F------7||||F---J.L7-||LJ|F7|LJL.J7J|7L7|-7-.--77J.F.FLLF-F.||LJ7FLF777LJ-L|FJ.--LLJJ.7F-LJ7-7J7F7|.JL-|FF-JLJJJ.|.L|J.LL|-FF7LFFJ..7J7-J-F.77|..7|LL...LF.JLJLF|F-LL|.|-.7FFFJF..7L|-.-F-L7.LF-F.L.-J|7FJL-77JJ-7|J7J-F-|F|F.F||L-7|7.F
# -F.L7.|FJ-F77J.|L|||L---7||JJ7F|||LJ7|-7FL|7...F---JLJ|||7JFL|J--.-LJL--LJ-|J.|...|LLL||.-|F|FFJ7..7-FF.-J.F-|F|FLFFL.L.F7J||77F--FF.||7J7J----7-L-7LL7-7F7--J77.7J7|L7F-.-7JLFF-----J|||-FLLLF|LJLJL---7|LLJF-F7|||L-7J-J-7L|L--LJ|L7-|-.77J-|--JJ.-J-.|.-L7-FL77LF----7L7.J.FJJFLJ7-F|||FFL|L.-J--7-7J-LJ-.F.--|FLFF--|77F|77JFLL7FF-F.-.L.|77J|-LFJ...-JJ7.LJ.7J-F||FL||J7JF.|J-J-.J|L-LJ-F7-FF.--|7|L77LL|FLJJFL-F7||F-JL-7.
# J..|L|.7L|.F|LL.FLJL----J||-F7.7LJL||J||7--7|J7L-7F---JLJ|JLF-|||J.|-|.L.F-||J.-L-.|F7-LLF7-77.JF|7L7.7L-L7JF-7-..JJ|-77F.-LJ|JLF.L--||77|J.---J7|J7.L-7|77.J|.J.|J-|J|7.7J7FFJL-7F---JLJLFLJ-LL-7F--7F-JLF.FJ|||||L--JF-|FLJJ|LL|7J7FLL.-7J.7.F-.F-FF-FF.7LJL7L|-||F--7|LF|J|FJFF||L||FF-F-7LJ..L.FJ7-7LFF|7|LLF|J|J.J-7-JLJLFJL-7.|L7-FLF7FFJFL7.-LLJF7.JJ-J|||-7L|||-77JJF|..LL.|7JL---|J|J7|-F.-L|L-LF-7|LLL77JJF||||L-7F7|J
# -L--7..-|J|.F...JF------7||7.L-JL7J-FF-77F7L.F---JL---7L|7FJ.-|7F.FLFL7--FJ.LL-F.7|J|.FFF-F|L--.-7|J|LJ7.|LJ..F77-|L--J.-77J-L|JL-|J7J|.J--F.LL|-7L7J-|||-FL7J.|F--|7L|||FFF-----JL-7L--L-JFFJ|-F||F7||J-.F-.F-J||L-7LLJL|L-...FLLFL..7.|||F7|J.-|7|7|.F-7FJ.L7.JF-JL-7|L-77.F7.|FF|JLJF.-||JF.||.JFLLFF7..|-.|F7.LJ..LF.-FJL|FLF.JF-F77-FF|FLFJ7.J7|-F..L7|FJ|-JLL.7|.7-JL|77|J..-L.J-FF7.F|.F.-F7.FL|J|.|.L|.L|F7|J|LJL--J|||J
# --7|L-.|LL.|.J.LLL-7F--7|||7-J-||JJ7|7L7-L7..L---7F---J|J.F|J7FF.7.-L7.F-J-L77FJ.FJF.J|.L|J.FLJ.|7-7JJ-.LFJFLFL|7J7.---7LF|F.FFJ||L|.JL||.J7-7JL||F--F|JL77JFL-J-|L|-|-J|FFL-7F7F7F-J|.-LJL|JL77JLJ||||J7.L..|F7||F-JFF|L7LLJ7L.7--FJ--.|-F7-L.J7L--FLF-F7F-.7F77L-7F7||F-J-|F-F-JF7-J|7JJJL7J|F--.L7..L--7LLF|-L--|-.F77.F7.7LJ-7FJ|LJL-7L---|||JLF-FLL-L-.F|FLLL|77L|||.|7F-J7|-L|.J-J.||..-F-7LL---.F7J-|-.|..F|7.L-7F---J||7
# FF.7LJJ7J7L7J-.JFF-J|F7||||-7|J7--7FJ|7-7FFF--7F-JL---7JL.-J-7..77J-JLFLJ|JFL7L|J7.77JF.JF||7FJJ|JL|.7JJFLLL..-|J.7F.J7-.|F.FJ|JLJ.JJ|--|-|L|.LF-.-.||J-|L-|F-LLJ.L7FF.J.F--7||||||F7L.L.F.7.FL|J.F||||J|J7J7|||||L-7...-L.7-LFF-7LF..--L.JF7F.-|7--7---7..JJJ-FJF-J|||||LF7FJ7.|-JF7LJ7JLL7.-FL7-LL.--|.F-7-J.JJFL7.77-F7--J.|..-L-.|.L.-|-L7F7FJF7L|7FF7|L.LLLJ|L||..|F|7.J-..-||L.||-|J.J7JLL7JLL.7.LF|JJ|.|F-|F7-F-J|F7F-J|J
# FLJ7L7.FFJLJFL-JL|F7|||||||L|FLFFLFFFF|-.-7L-7|L-7F--7|.JJJF-|LL7FL7L7|JJ-|-||LL7-7F77J7J|.|F-F.-FJ|..FF.L-L..-F.7.J.LLF7FL-7L-|-..LL7..|7LF|L.JF-.L7.-||J...J.L-L7.LJL..|F7|||||LJ.7|J7JFJ.-.F-|7.|||||JFLFL||LJ|F-JFJJF|---LLF7|J7FF7FL7|L-J-L7FJJ7|..F|JF-.L77L-7|LJLJ-F.L.F.JFF.-F|L.FL||FL|..7L7-.J77.FJF-FJFFJJ7|.7|F7J.J-JJ7|FJF.LL7F|LJJFL7L7JJJ7J.J7|J7.-JFLL7-L||L7..|J7.J|J.L-.-|.7F77.7L--7FLLFJFFL--|.77L-7|||L-7|7
# -.-..FJ|.JJJ.JLJ.|||LJ||LJL-7JF77L||-LL7-F---JL--J|F7|||.-LL.LLFJF7-F|-|-|7-J||.|||JF7.77FJJL|77|...7J7.-LFJ|-7J7-FJFJ7F7---LJJ.--7|.LJ|JJ|J7JLFLJ7L.|777FL|LFL7F.7L7--F7|||LJ|||LJ|F.7J-77F.J7-.-7|LJ|JF.L7.||F-JL-7J7.L-JL7FL-7FF|7JL7-|FL||F7JJ|J---FJJJFL-L.L..|L-77|7L7.LF.JJJ.FL---|F|JFL.J7F7LF----7.7-F7L.F-F-L|JJ||-||L-J.7FJ||.FJ77.77J..7F|F|L|-J7FLF-|-.|L.-L|77-|77||J..|7L-LJJ.LF||F-.J|7.7FL---7L||L-LF-JLJL-7||F
# LJ-JL|7-F7|.7J-.FLJL-7|L----JL7J..L7L7F|F|F7F--7F7|||LJ|F7J-|-L7FJJ7JJJ..|.F.LF--|F7.JJJLFL7LF.7|.|L|F7-|7LLFJLLJ|||JJL7-7F7.|J7F|F..FJ.-F|7F|7J7--LF7..J7.-F7JLJ|-F|JJ||LJL-7|LJ-FLFF7-F--LF|LJ7LJL--JJ|FL|-|||F---JJ.7.L7|-J7|FL7J7-L7.J||F.JJ..J.LFL77LJJ|-..||.|F7||F-|.F7-|JJF7.-.-|7L--F77LL|FJL---7|FJJL-|.LJJ|LF7|.JLLL.-L-FL.FJ|.|7F.-|7|F|J-FL---F7J7JLLL.F-|JJJ.|77-JJ7.JJ7.J.FJ7J7L7-L77LJ|FLF-F|F-J.7|L7L-7F7F-J||7
# .-7L|-|7..L7JL||FF---J|F----7J7|LL7F|-J77||||F-J||LJ|J.7F7LJJLJLJ.F|J-J.LJJ.-|L--.-J.7.FFFF|7F|FFLL.LFLL-.F7L-.|.-J|-|7JJ|J|77.-J.7-LFJL||F-JF7-.7||-L.F||-JF7J|LJ.77F-JL----J|LLL-.-|.|J|7|J-|||.-F.7-FJJLF7|LJ|F7F|.J7.|..FF7|.J..JF||L7L|J|JLJLFF7LJ..FJ.-JJ7LJL||||LLJ||-77.J--||JJ.----.-77FFL7L.JF-JL-7|-..LFL.7|-7J-F||J7FJ7J|LL-7.7-7.FJ7LL.J7L|J7J7|.77.|7JL7|JJ.JFJ.-|7L7F.|77-J7-F.|7FF|FF-|L|FLFL|-J---77F-J|||F-J|J
# L77FF--7.FF7FJ.|J|F--7|L-7F7|-||J7||FLL7J||LJL--J|F-JFJ-|7L.J.JFL|J7J.-7.FFLL|7|FJ.LJ.7||.J7F7L7-L|-7.LJL.F.F77J|F.-F7L7.J.-LFF7L|JJF--L7L7FL7F-|JJLL-.-FL||-LL7L||F7L---7F--7|--JJ|FF..7-7|F|.7.L7J||-F..-|||F7|||FF-7.LF|FLJF-.JF.-F.JJ.-F.JJJLLJJ.J-F|-7L.-LL-JJ||LJJF7|-FLL|JL.-L7J.-|..FFLL|-J7.JL|F---J|-||L.-|7.|.LFF-.7..-J-7FJL|FJ7-F.-..|LLLF7-.|F.-777|-.-L7||L-|7|..JLJ.FFJF.--|JL|-.-|7F|J7.J7L7.||||L-7|F7|LJL--J.
# .FF-J.|F|.J|.7|F7||LL|L--J|||J-L.7.FLF-F-J||-F---JL-7..7|F-J.J.--FF|F|LJ7|.J|F|-LJ7F|-J-J.7-7F7LFJ-FL7L7|7|.LLJJ7LF-..-.LL-77L.F.77-L7-|7F|-FL-LJFF--77JFLJFLLF-JLL..F---J|F-J|L77-F|L-LF7.LLL7FF77L.L77LL.|||||LJ|JFJ|LF.|FJ-LF|FF|.77.L|-L.J7.-F7|.L|.LF-..7-|LF7||L-F-||.|...LLLF|JLJJF|L....L-FF---J|F7||7L7||-|J7.L-|-.|F||F7L7L-F77-L|-7J7FL7..F-J.F7F..J.LJJ||LJFJ7J-L|7J77LF.FJ|F.LJLJL|-7FF-LL.F.F-7-L|FJJF-J|||F7L|77L
# 777J-L..F-FJ-FJ||||7-|F---JLJJ--.L7|F7-|F-JF7L---7F7|.|-7.L.7J..7F|FJFJLJL-.J-LJLL-F|.7||L-FL77.J.LL.JL|L77L7JJFFL|FJF...F7|L-7LFJ-J7LF7JL|F7.L-L|F|.7.|L|F-FJ..7|-..L----J|F-JFFJ7-JJLLL-77L.LF77-|7LL|LLL||||L-7|7-.LJ--|F77J7-L-F7|L|-JJ-7.JLF7FJF|LF77-F7L7..||||F|77.J-7J|F...|77|-.FJL7-|L-F|L---7|||FLJ|J.77-.||L7|FFJJ-.7----7---|L7.7F-||FFJ7-7||JJ|7L-7.7|-FLJ77J--|7|7FF-JF|J|LLF|FL7-L.-||7.|L-|JJ||77|L-7|LJ||F-J|F
# .J||.J.F-JF|LFJ|LJ|.L|L-----7LJ...J|-F-J||LF----7||||-..7LL.|-7J-LLF7F----7F7-.J|F7F7F--7F7LLF--7F7|JL.F7F----7F--LF----7-|-J-LF7F7F--7..|-L-F7F7|L-7J.|-7|.77JJ-FLF-------J|.-||-..J.7J-.JJJ7JJJ|7J.F|L.|7|LJ|F-J|7|.-F7F7F----7JF7J-LF----7F77-FJF----7LL|FL.--|LJL-7|FF-.J|-F.F----7F7F--------7F---JLJL-----------7F--7F7|.FL|7F--7F--7J..J7-F----7F77LF77|L|7JJL7.LF7-|JL-L-F--7F7|JF|.7.--FF7F----7FL.JJJ7||-F-JL--J|7J7L7
# LJ.-LFF-.JF|.LJ|F-JLL|F----7|-|.L-7|LL-7|F.|F--7|||LJ||JLJ7.FJLL7FF||L---7|L-J-JL||||L-7|J.L.|F-J||J|77|||F--7|J--.L-7F-J|.L7FF|||||F-JJ.-77J||||FLJ|7|F|F|7LL-L7.LL-7F7F--7|FLLFLJJ|.F..-J-|FLF|FJ7.|-J7|-L--J|F-J.J-F||||L---7|.-.JF7L---7|||L|-L|F7F-JFJ7-7JJ|L---7|.|7.J|.L77|F7F-J|||F------7|L-7F----------7F--7|L-7|||JJF.J-|F-J|F-JLJ|J|.|F7F7|||7FLJ-.J-||7J7-|.7.|LF|LF|F-J||L7LL|LL7.-||L-7F7|FJ|LL||.JJ|F--7F-J7.L|J
# L.J.|LF7FJ|FFF7||LF.J||F---J|-|7.JLF---J|-|||F7|LJ|.LJ7LL||-|L7F---J|-|F-JL-7F|F7|LJL--J|7FF-J|F-JL----JLJL-7||7-F7F-JL---7F|F-J||LJL-7||7JJF|LJL-7J7LL---LJ77.|FFFF-J|||F-J|7L77-.7.-7L-|-.7J7JL.-7|-.L7F-----J||7FLF-JLJL----J|.7J7F7F7F7||||JLF-J||L---7FLF--7F7F-J|-LFJ.LJJF-J||L--JLJ|FF.JJ-|L-7|L-77-|J|7|J|L-7|L--JLJ|F.F---JL--JL-7-|F---J|||||||F||F-7-.L.|..-L|F------7||F-J|..F|LJJ-F-JL--J|||F7-L|JFL7-|L-7||7-|-J|.
# L-|7J.F.LJ||.||||-|-7LJL---7||.-J7.L-7F-J7FLJ|||F7|..-F|.FJ7JLFL-7F-J-.|F--7||.||L-7F---J.|L-7||F7F7F----7F-J||J7||L---7F7|L-|F-J|F--7|L-|7|-|F--7|-JF7|LL-||-LLJF|L--JLJ|F-JJ|LJF7-7|F|J-L77F7-77LF-7.7JL---7F7|.FLF|F------7F7|J|7L||||||||||7-|F7|L-7F7|-.|F7|||L-7|7F-|JFLL|F-JL-7F---J-7FF7-L-7||F-JJLJ|L-FF|F7||F7F7F-J.7|F--7F--7F-J--|F---J||||||LJLL-L.7|LL7JL|.L-----7||||F7|JJLJ.-FF|F----7|||||...J-J--|F7|||7.-7F|-
# .-.-FJ||-7-7J||||JF.|F--7F-JL-7L-L|F-J|L7|-F-JLJ||||.7L7L-..LF---J|7|F7||F-J|F7|L--JL---7F---JLJ||||L-7F-J|F7|L--JL----J||L--JL--J|F-J|7.7L.F||F7|L-7J7F7.|-J|.-FJ|F-----J|.LL-.7L---.FF..7.LJ7L.7.J7LJL7F---J|||77F-J|7|F---J|||-JF-JLJLJLJLJ|F7|||L-7|||L--J||LJ|F-J|-|-FFFF-J|7-|L|L-7FJ-.F-.FF7|LJL-7|-F.L-F-J||||||||L----J|7|||F-J|F--7||.J|J||||||.LJ.L.7FL-|F7.F7F-----JLJLJ||||J||L|F-J|LJJ-|||LJ||LJ.L|F-J||||||7..L.7
# JL-.-|FF|.-F-||||7.F-L-7||F--7|-L77|F-J|L||L----J||-|7LF7.LFF|F7F-J|7--||L-7||||F--7F7F-J|F7F---J||L--JL-7|||L-7F7F--7F7|L-7F----7|L--J.LJ.F.||||L-7|FJ|L.7L77.L-LF|F--7F7|7FF.J|-L7F7|FLL77FJF|J|FFL|-|F|F--7|LJ-F|F-J7||F---J||F.|F--------7|||||L--J||L----JL-7||F-JJ|.F..L-7|-F|.L--J.J7JLL|||||F---JFLFFJ-L--JLJLJLJL-7F7F-J-.||L-7||F7|||LF|-||LJ||F7FFL|.|LJ|F|.||L-----7F7F-JLJ77FL.7L-7|-|FLLJL-7|.J|FL7L--J||LJ-L--|--
# ..--77L|LLL7.|LJ|7-.7F-JLJL-7||FLF-J|FJ||F7F----7||FJFL7|F7F-J|||77FLF-J|F-JLJLJ||L|||L--J|||FFF-JL---7J-|LJ|F-J|||7|||||7F|L-7F||L---7F7-JF7|LJ|7J|L---7-F7---|-F-J|F7||||J77FJJ||LL.7|L7J|J.7.F7JLJL.-7|L-7||F---J|7|7J||F7F7||F-JL-7F7F7F-JLJLJ||JF-J|F-77--F-JLJ||FJJJ7F---JL-7FJ77FJJFJFJJF-J||L-7FFLFLJ7|..7JL-F-----J|||LJFJ||F7|||||LJ|-FF7||F-J|FF-7.-.|F7L.F-J||.LLF-J||L-77J.||.F---JL-7||777F|L-7|-.JF---J|-|JF.J7JL
# |7LL.-7|F-J7J|F-J.F-7L-7F--7|LJF-|F-JF||-.-L-7F-J||JFJL.F|7|F7|LJJ.JL|F-JL------J7JLJL-7F-JLJ-LL------J||L-7|L-7|LJ-FLJLJJ.L--JLFL-7F-J||-F|||F-J-FL---7|F7JFJ|LLL--J||||LJ.LL7LF-LL|.|L.J.-77||7|.J-|-7||F-JLJ|F7F-JFL--|||||||||F---J-J|||F-----J7JL--JF.L.|J|F---JF|JF.LL-7F---J.J|FF7LJF|77|F7||F-J.-JFF7.--.-7-JL-7F--7|LJ7FL7LJ||||||L--J..|||||F-J|FLJJ7|--7.J|F-J-|.FL--J|F7|.7-|F7|F7F---J7|J.7.L-7|F|F||F---J7FJ|-7.-L
# LJF7.J|FL.|F-J||7-LJ-F-J|F-JL----J|JLLLJLF7F-J|F-J|JLJJ|LF-J||L-7.FF-JL-7-FLL-LL|F--7F-JL-7|F--7-7F.|-.F7F-J|F7||J.L.|-FLJFFF|FL-F-JL--J|-7|LJL-7L-7|7L|L---77FFFF--7|LJL-7JJJ|..J-F.-L|-|F.-|L|-JF7L7LF-JL----J|||.7J-F.|LJ||LJLJ|-.L.F-J||L---7F.J-7JJJ..L7F-J|F--7FL.-7-F-JL-----7J|LJ-|-JL7|||||L-7F7...LFL|-77--F7|L-7|L-77.|FF-JLJLJL-77L.-|LJLJL-77J-FL..J.JF-J|7LF7JFF---J|||-FJJ.J||||F7F--7J7JJF7|L----JL---7FFLL|F-JF
# .7L-.7||LL7|F-J.J7.-.|F-J|F7F7F--7|77.JF-|||F7||F-J7--L.-|F-J|F-J7||F---J7.|JF7J-|F-J|F---J--J-.|J.-FF-|||F-J||LJL7F|7|LL--|7|.7F|F7F---JLJ|F7F-J|LLLL7L---7|-|J.|F-JL-7F-JLJ-LFFF.F|F|7.L|7-.LLF7J7|.LL-7F7F--7|LJL|77LJ|F-J|F---J7-J|L-7||F7F-JJFLFJLLL7-7||F7||F-J.|L|JLL---7F7F-J7.7-.J7FF|||LJ|F-JF.L..7||--7JLJ||L-7||F-J|L-J|F----7F-J-L.JL-7F7F-J7-|.|.7LJL|F-J|7FJ-||F7F7|LJ|.LJ7FLJ|||||F-JF7|.JLL-----7F7F-J|7FF7JJ.J
# JJ--.|F.L.L|L-7.LJ.JL|L-7||||||F-J|7JL7-7|||||LJL-7LJ-|7-|L-7|L----J|L-|JLF7..-7F|L--JL-777-||JJ|L7F.|||||L--J|F-|F.|||.J|-LL|.|F|||L---7LF|||L-7.77LLFL77L|L----JL----JL-7..-7-F|LL|F-L..L.-7JLLL.F-J|F7||||F-J|-JFJ|.LL||F7|L-7777-7.F-JLJ|||.JL|J.J77J7.L-|||||L-7F||7.L7FF-J|||F7.-7.L.-7L-|L-7|L-77J..|JJ.FLJ7F7|L--J|||F7.LF-JL---7||-F|FF---J|||-L|J-JJJFJF7||7-JJJ7F7||||||.|7JLF7.7||||||L-77LFF77JLF7F7||||FF-JJ|JL|J|
# LFF.|77J-J||F7|.-.7F-L--J||LJ|||F-JJJF|.-||||L-7F-JJJL|-JL-7|L------JJ-.|-LL|7|7J|F-----J77FJJ.LJ|--7J.|||F7F-JFLF-.FLJ7J-FF7LFFJLJL---7|||LJ|F-JL.J...J7F.L---7F7F7F-----JLJ|-F-LF..|J|LFJF7LL.7.FLL7J||LJ|||F7|F|F7FFFL|||||F-J-|.7|-|F7F7|||.L|JLFJFJ7||JF||LJ|F-JJ7F.|.J7|F7|LJ|||L|L|.7L7JL-7||F-J-FF7FJL.L-J-|||F--7|LJJLJ-|F7F7F7|LJ.FJ.L-7F-J||JF|L||.|JL||||7..L7F||LJLJ||FFF||L7J|F||||L-7|.J.7F-LFJL||||LJ-LFLLF||FL-
# FJ|7L|JL-F-J|||-7|77L.7F-J|F7||||F|-|FJL||LJL-7||F7L|7LF7F-J|F7JJLL.JL||FJ7.FFL7-|L-----7-|7FJJ|F-FL|-.|LJ||L-7|-7LLF-J|7.|J.7|FJF----7||-FF-J|L7..F|LL|L.--JJ||||||L-7F7F7-.J7.F.7J--LLJL7J-.L|.--JJ|L||F-J|||||.L-.F|F-J||LJ|J..JL..J||||||||F|-FFFF.LF|FF-JL-7||77|.FLL||-||||F-J|F7.J.7.|F--7|LJ||-FLFLL7..-L7J|LJ|F-J|7||F..||||||||LLFFJFF7|L-7||LF.7||LJF7|LJ|||.L.L||F---J|-L.J..-JL||LJL--JL-7L-.-J|.F|LJ|FF7J|..LF.7F7
# FF|L--||7L-7|LJL7.J.L.L|F-J||LJLJ.FLL.||.|F7F-J||L7.|-J|||F-J||F|7F-|-F-|-|.J|FL.L-7F7F-JL|F-|7|J.|L.F||F-J|F-J7.LL...F7||..7|J-L|F---J||7|L-7|L7FL||JJF.7J7-|LLJLJ|F7|||||FJ|LLJ|7|..|-J-.L.|LJF.7.77F|||F7|LJLJ-LL7--|F7||F-JL|JJFLF|LJ||||LJLJ7J7LFF.77||F--7|||-J.||.|||7LJ|||F7|||7-L|L||F7|L-7|F|FL---L||L.FL|F-JL--JJJ|F-J||LJLJLJJ.7-7-||L-7|LJLL|-..-|||L-7|J77|..||L---7|LF.-7.LL7JL-7F7F---J7F.7|F|J|F7|J77-FJL-J-.JF
# 7.LL-7FJLF-J|7|JJFLL-L7|L--JL-7FF77.J.|F-J||L-7||J||-|F|||L-7||7FJ.|.|F7LL-7-JLF7F7||||F-.F-|--FF7F.|F-JL-7||JJ.|-L|.LLF|-J|FL-LL|L----JL-7F-J|.J--F||7L-7.F.-|L-F.|||||LJL-7-L-JL7.F7|L7--L7LJF--77.F-JLJ||L-7.FL.J.F.|||||L-7F7FJJJF7F-J|||7-7L..F7--LJ-7|L-7|LJ|J7|J|J-J7|..|LJ||LJL-7.LJ-|||L--J|.LJ7L--7J|JLF7||F--7L.JF.LF-JL-----7|J7FF-JL-7||77F.L.-.F7|L--J|J-J|F-J|F---J|F..-J7FJL-|7||||F----7LJF|F.||||.7.JF7-|F-7|F
# |7|7JJ|LFL-7|-L-L.LJLLLL-7F--7|LLJ.F..L|F-J|F-JLJ7J-7L.||L-7|||L||.7.7F.-7F-J..||||||LJ.LF7.JFF.7.|F-L-7F-J|||7J|JJ-LL-FJ|--7..J-L---7F7F-J|F-JF7--JJFJ|-|LJL-7J7-.||LJL-7F-JF7F.-J7|-7F7-.-L7L|F-JL.|F---J|F-J|FL-....||LJL--J-7L---||L-7|LJLJLF|7--LFFJ-.|F-J|F-JL|.L|LJ-LF|7L--JL-7FSJJ.L7LJ|F---J|L77|-77LL|F|||||F-J7J7L|FL-----7F-J7-.JL-7F7|||L-7-|J.J|||F7F-J7J-FL-7|L-7F-JJ||L7L..JFFLLJ|||F---JL-.7||||LJ|L|.L|.JJ.-.L
# JJFJ.7|F7F7||JJ7F.LJ77JF7|L-7||J.||JJF.||F-JL-7F7F.|LF.|L--JLJ|7F||J77.JFFFL|-F|||LJL-7|7-FFLL.-|-L.|F-JL-7|||-FJJ-JF..FJ|7J7F|FJF--7|||L--J|7|-|7J7JFFFFJJFJ7-7JLL|L-7F7|L-7|7.F.FLF7J77JL|LF7||-7LJ|L---7||LJF7-F7|.F|L---7L77-7FJF|L--JL-7FL-F|-7|7-J.J.|L-7||7LF----7FJLJJJ|LF7F-J|..JFF---JL-7|7F7F--77FL-.F|||||L-777F7.JF--7F-J||..L7LF7|||LJ|F------7|LJ|||-.7JF7F-JL--J|JJ|..7.L7LFL|F|||LJL-77-.JFLF-J|F7F7J-.7LJ|.L|7
# F|LLJL-J.||||LJ-.F.F7|L|||F7|LJ.L7L7-.FLJ|F---J||..7..LL---7F7|.7||JF7|7-L-7||J|||F---J|FJ|J|FF.-7.F.L---7|LJL--FL.J7FF..-FJ-|7|FL-7||||F--7||.J7F7|J..FF|LL-JL-|-LL-7||||F-J7L777F|.-L-|-.L.||||J.F|L---7|LJ.J-7JF..|JL-7F-JLJ|--|.||F7F---JL-.|-.7LF.7.L-L--J||7||F--7|.7-FF-J-||L-7|7-7LL---7F-JJJ|||F-J.F7.-||||||F-JJ|J.-7|F7||F-JFJF777|||||F-JL-7F--7|L--J||-7-L||L---7F7|7FF-F.-J|-LF|-.|L---7|.|J|-J|F7|||||7F7-FLF7FF|
# .7JLLFJF-JLJ||.|.|7.FJF|||||||FF.JL|.-LF7||F---J|F|.F|7F---J|||F7|.F7F--77.|7F-JLJL-77J.F.-FFFLF.F-F--7F-J||||L|F.7.-|-|.L|-7|L.LF-J||||L-7||F-FF-77.|F7---7F7-JL7.|||LJLJL-7F7FJJJ--J7.-FJF-JLJ|7JF|F--7|L-7JLLL.---F---J|L|-.7L|LF-J||L-7.JJ--J.7FL7JJ.F7F7F-JL--J||-|L---7LFJ7|L--J|F||JF7F-JL----JLJ|LJ7|-JF-JLJLJ|7FJ--|F-J||LJ|-L|7F|F-JLJ||L----J|L.|L-7F-J|F---JL-7F-J|||F----------7J.|FF---J||.JJJ.|||||LJL-7LFF7F7F|-
# -J|LJ.7L-7F7|77|F77|7.-||||||J-J-FL.J.||||||F7F7|-JLF|7|F7F7|||||F||||F-J.|.7|F--7F-J7L.LJ--7J7-7.-|F-JL-7|7|.F.F|F..J.J||J7LF|J7|F-JLJ|F7|LJ77.|-7F7L7-7JF-L|F||-.J.L-7F--7|||L.LJ.7|..7.|L-7F7|-F.L|F7||F-J.|F7-7|JL-7F-JLL-LF|-7|F7|L-7|-7L7JLJ.--JFJ-|||||F--7F-J--L-7F7||.JLL-7F-J7LJF||L-7F--7F---J..F.77|F7F---JJJJLFJL-7|L-7|7J..JJL---7||F-----J7-L-7||F-J|F7F--7||F7|LJL-7F--7F---J7|.L|F---JL.J-LL||||L-7F-JJ.|.J||.7
# -|-FFF---J|||-FL.FLF|.L|LJ|||7LLL-JJJF-JLJLJ|||||..LJ-J|||||||LJL--JLJ|-LF|7-||F-JL-77--7L7.|JJ-LJ.|L----J|-|F.J-777-J..7F||7JJ|L||F7F-J|||LFFLFF.L|.FLLFL-L..L|.LF-J.-|L-7|LJL-7|FF.-|F-----J||L----J||LJ|J||FF-------J|J-.-J||FL|||||F7||7L7|J.L|.-.J7||||LJ|F-J||F--F-J|||F-----J|-JF-LF|L--JL-7||.7.-|F-L.L|||L-7|JJJLJ.FF7|L-7||..-L7JF---J||L-7|JF7-FF-JLJ|F-J|||FL|LJ||L----J|J7|L---7F7F-JL-7-F7FLFL||||L--J|L|-|LJFJ.|L
# ||-.|L-7F7|LJF|---|.7-|L--JLJ.|J-.J||L---7F7|LJLJFF.|J.LJLJ||L-7F-----JLF||F7||L-7F-JF77JJ||-7J.LJF|F7F7F-JF-77|.L.|77J|L-F-L7-.-|||||F-JLJ--F7-.FJ7J|7-.7|J-L||F7JFL|7L--JL-7F-J|J.LJFL-7F---JL-----7|L--J..||L-7F-----JJ|L.F..|.F||LJ||LJ|F-|JJ.JFL-.7||||F7|L--J-.FFL--J|||F7F---JL...F-L---7F-JLJJ|LLLFJJF7|||F7|-7JJ|J77|||F7|LJ-.L.7JL-7F-JL--J||F.JJ|F7F7||F-JLJLJ|F-JL-7F---JL.L-7F7||||F---J.7|.L|..|||F---JFJ|7.|7JLF-
# -F-----J||L-----77|7||--|77LJJ-JJF-------J||L--------------J|F-JL-7LF-|L.LJ.J||F-J|J-7..LF7|7J7J-.F||||||7J.FFL|LLLJ.J7JF-J.F7.J|||||||F77FLJLLJ|L-F.-L-.7J.|J7.JJ-|L-|7.J|F-JL----------JL-7|7FJ-|--|L-7|LJF-JF-JL-77J7.J.FJ7-FJL-|L--J|-F---J-FJ7F-J-|L|LJ|||--L..F7L.7F-JLJ|||-|-|FF---FF---JL-7|J|LL.7.J-J7||||||J-.L|-F||LJ||||-JFJLFJF-JL-7...7.-FJ-L|||||LJ|.|L7L.||F---J|-F|J.7F||||LJLJ|JL7-|.||-JFF|||L---7L|-LFLFJL-F
# 7L------JL------J.JF--|LJ.J7FLF-|L--------JL----------------JL----JJJJJJ|FJJFLJL--J7J------|FLLF.J-LJLJLJ-..LJ.|LFJJF7|.|F7|..LJ.||||||||.LLLJL.|J--.L--77-JF7JFF7-JL7|L.7LL----------------JJ7F|F7|JL--JF|LJ|.L----JLF.|7J|7|-7-..L----JLL-7LFJ|JF|7JFF7L--JLJ||-7...L--L----JLJFL7L-7LJ.7L------JJ.-.7.|7JFFJLJLJLJFJ.-J.FLL--JLJ|-F..-F-L----J-|7-|JFJ-FLJLJL--JFLJ7LFLJL----J|L|7.|7.LJL----J--.F7|J7-||7LJL----J..|.LLJJ7|-
# -||JFF7J||-7LJL..L|FLJ-FLFJFJ|F7-LFJ..|J7|.F.-L7J-.L|7.L7L7J-|77FJLJ|J|L.7|7-.J7.7LJJLJF.|-F77.7-7L--|JL7F.-J7JJ7JJ77|L|-F|L|L.-F|LJLJLJ|L.|7|L|L77F|FJ7F7L.7FJJ|J.LL.|L-777LLLL-JL-L-|--.|-.7L|FF7||-|..JLLFL77|FFL|JJF.-.FL--L.7L-7---JLL7LF--J||FF|J|.|L|FF|L..F.7.FLL|7JF7F.7L7.F-.-77FL7.LJ.|JL|JFL-|-F|J|JJF|.|7J|-7FLFLJ.7.-|.FLJ--J7L|-F|.7LF||-7J7|F-|LF|.7.FJ-7F.7-7-FFL7-JJ|7|||.|...JL-L|7.7J.L|F....J|LJL-77-|7.7J.
# J-FLJLF.-|7|7-F7JLJLJ7-L.7|-L.|JFJLJ||..|-JF-|7---|7-.7FLL7L.JJFF-J7.-FL|J|FLJ-J.|-LJF-7F-J|L7J.7F|-FJF-LJJLF7F.|J|L-777J7.F7-JLFL---7F-JL.JFL7-L.L.-.|JFJJ7F-|LL|F7L.-FL.||L|JLJ.LLFJ.F|-7F.77L-FFL-J|-F7L7.|.7FFFLJLLJJLL||J7-L|.J.J77-L-.7J.L-77LL7|7-LF.L77|--L.7.|J77F.-|.F77..J|..7L||.|L|L--..LFJ7L.-|7JLFL--FJ|.-JLL-JLLLJFJ.-JF7JJ-J|-FJF-FL-||FJL|JL.L|.|.F.JJ.-|-----LLLFL77..-7LFFJL.7.FL.JL-J..F.|J|F-7||-.J-J.J-F.
# LJF-..JJ|.LJ7-L|7.|F.77-7-F-||L7FJ|-7-.J.LJFJJJ7LJJL||J7LLFFL.F|||-7L7|L7|J-7.|.77FJJ-LJ7|FL777|L-J..FFL-F.JF|7-J7JFF.||.|J||.-F7F---J|-.7F.JLJ.|LJ7|--77|.J||J.|||L.-LL||L-.-J7.-|-7|--.J|-|-|-|FF..LF7F.|LJJ7.7.7J7FJ-.7-|..J|7J|.-L77F.7|FFL7.|.J|L-|7.JJJJJ77-FLJJ--F-LJJL-J|F||L7|FLF-.JJLLF7L|..7-L-|L7JLL..LFLL.J.F7LJJ-777|LL7||||7|.L7.F-J-F|.7-L|.|L7-JLF.|-.J7|J.-|JL||FJF777-.J--JLF.L7.F-7FJFFLLFLF---LJFL-LF|LF.F-
# .|J77.|JLLF-|JL7FL-7-7|J|-LJ.7F-LLJ..|.|LJJJJ|.F-L-JF7--.--LL77-.-|F|7JJ||JFJL--J.|J7LLJLL777L7.|.|7-..-7J.7F7F--|J.7|JLLJ-.F|..LL-7F-JF|FLLJF-L-.7L|L|-FF|7LLLJLF.7L..L.-|.-|.7|7J7L7.-|77L.F-77--|7JFL--.|L-|LL.-JFLF.J|--7L--L|7LJ|-.FFFJ7-J-F7F.LF.FFJ|FFJL7..J.LFJL.|777.-.-F|F|--.J.L.L-|-.|.F|L|7FJFFFJ7F7LF-J-LL-J-J|||LF.F-.L-7J|.7|-FJJ-J|LJJL7...LJ7|-F.7.-7.|-F-|FJF|F7.JJ|-L7JFL..J-J--F-.||77L77FFFL7--J77F-|L-7.7
# |77|--.7|FLJ.JF-|F-LJ.7.77-...|L-L7F.-FLF-F-||L7777F-F..-LFF7J..|..|-F-|F-J-F-JJJ|J.J.|JLF-..7.7|-J....F7FJ-L|7|..FJJ|-LF|77-7FF7F-J|7|||LJJ-||-|LF|L.J-FJ7-J|J7|||-J.7LLJLJ.J-7..7JJ|7|..FJ-.|L7FL7|FF.|F.FJJJJ-|7|.-F|.7L77.||J..LL|F|7-.--|L-J77-|.LFFJFL.L.L-LL..-|7|F.LLFJ7L|J77JFFF|J|.-F|FFJL7L.-.JLL7.FL|J7J|FLFL7L-.-|L|F-J|..F7|-.|JLLF|7FFJ-77--|F.-L|.|.7LF--F-JLFF-J.|7-.J|-JF|.JJ-.-7F--J-LLLL-L7LJJLJ7L|7-|7.-|F.
# |J-F|-|LL|FF|.F7|.|.-|-FJ.7J.|.L.-J77J7J..J777.F7-JLL..7.|JF||FJ7LL|F-7|L-|.|77J.||.-7-.FJ7L7L7-||7|-LLL.LF|JFJL-..JL||7-JJF-.L|||F-J-JJ--.FJ-7|7L|7F-J||J--J|J-77|J-F7L-.-JFL7J..L-||L777-||7--JJJ-LJ77-LL7-.L-7--LLJFJ.7F.-F7FFF|7F-|L..L-L7JJ7LL.-.7.JF.L.-J|LLJ7-7JLFJ-JL.LJFL7-..JJ77LJL-|J7J|7FL-7L.FJL.-|.J-7JF.J|F.7F.|7|FLF||7LLJJ|J7JJ--||FF|L|FLL.--J|7.F7J.JLJ--FJJ|.J..|7|||---7-JF|.L|-.L|-.LJJ|FJF7|.-FL-J7-F.|-L
# |FLF7.|.F.|7|JF7FL..--|FFL.JL7--L77F7|--J-7-|L77|JJJ|7LFJLL7L|7|7-.-J-7.JJL.-FFJ..7.-|77L.FJ..F.-..|.-|.7-...7F|-LLJ7.|7|J|FJF7|LJ|J77J7-J7.7L|.J7.|LJF-.LL7LFL|L-|L|LJL.F7JLJJJLJJ-L-|.|J7|7LFLJ-.-FJ777L.L.L7.L..|LJ---L|||JFF|.J7-J|L.|.-JJL77.--|JF.L-|7L|J7||JLLLFL--.|7.-|-L.F7.|.FF.-77J.|-JF.L||L.L||J-JL|L7J|JJ||J-LFFL.-..FL||--FF-.J|FJ7LFFLL|JJ|7JLF-LJL|7LJL-F|--J.7LL-F-JLJL.LL7F|..|.J|JJ-|FJFJ|FJ--.L.-|JJ7..|J|
# L7--L7FF|JL7|-J7.JL|77FJ|L-LL.|.F777.JF-JLJ77|.J7.|-L7.JJJL-F|LFL.F-.L||L|.7LFJFLJ|--L|7--.L-.JFFL-77L7J7J.-7FLL..7FF|.--7||-F.|F-J||LJFJJ--F|--.-FLF|.J|-L||-.LJJ77JF|-77.L7-J--|F-77.7LL-J7J.FJJ.JL|7FFF.7.7|L.7L7-JLF|-L|-FF|-7F-J|F7-LJ7|-J-.7J.7L..JLJJFL.7||-7F-J-JJJ..L.FL-|7LLJ7..-LL||7|.|-|L-|FFJ.7J-|-LF7L.LLL.-77J-LFFF.7..-J-L|J--FJ7.JJ||--L.-7-FF.-F|7.LLJJFF.-7.--LFFF|.J-||F.7J|J|7F7J7.J-.7---FL|F.|J-.FF.-J-F
# LFJLF7F-J--F||J-7L77-L.L.FF-7-7-L.-J|||-|||--F7JFFJJ.7F|L|..7L.|F-F7-|-FJ777J-L|.7.-||-7F-F|F|--JJ--.77F7|L--J.FL|7FL77FF|..FF-J|J--..-FLJ.LF|JF--|JL||-.|.J-J|7JLJL.-L-|.LJ|F-.J7|.LJ.77-|J.F||7F7F7|LLJL-.-L-LJ.-JF7FLF|-F7J.|J|777777|J-LL.L--||F77.||-F-.L-F-.LJ|LF7FJL|--JJ7-L-FFF|J...J-F7L.J-7|FF7L.||J|FLFF-.J7.|L|7FJF77JLL.FF7.-||FF.|7JL7J.FL|7-L-L7L--|FF-.7LJ--LJ.J-F..F..J-L-.|F|F-7||7.L.FL-F|JJJL.F.7|7||FL-.L.|
# 7F--.77-F..-|J....L-LF-||.J|-F7.-77.FJ.|-7.J7-JLL-J7LL||.||-L.FFLJF77FJ|..LJ-J-7JF-|-JFF|-.J|LJ|FF|LF.|7J.7-LL.J-FJJ-|J||F.|||F-JF7|-|-.F.|J-L7L|JLJ7L77F7L.--FF-.-.L7JJJ7|JL.L7-.|J|J.JF-FF7..J-|-F7-|7JF7.LF|.|-|JF||||F77L7|-7-7|L7--J.LJ777-F7|||LLLF7F-|.-.JFJ|-7.JJ-F|.JL7|.JJ7.-7.F.J|J-||F----L-FJ.7||FJ7F-7|.|-.JF-|.|J--F7|-7JJ7-FJ-|FJ7-LF7.-.7||JJLJF7JJ.|.|LF|.F.JLF.-.J|FF|L|.-J7--J7..LJ.J-JLL77L7LF|-LF-LLFF||7|
# J.--7|-JFF.777-F7-|L7J7.L-.FLL77L.|J7|FFJ-FL7..|..JL.|J-L-|.J.LLF-FL7L|L-7L|JJFF.JFF7J7JFJ77L|J7--7FFF.L|-77LL||L|.F7F--7JFF-J||FF-L7L7JJF77.LJ|.L.--LFJ|L.7J.|JL77L.77FF-.7.|7.7-F7.J|.LJ|7-|.--J-F.--.F-LF-J7LJL|J7.JF-J.FF|.FF|..LJJ.J-FFJF7|F.F|J7LL.L.77.JF|L7F7JJFL-|JJJF.L.F.J7J.|.L.7LF.|J-.F.JJ-.F.F.---..FJ7-F.|L|FFJFJ|L||-.F|L7--..-..-F-JL|LJL.FFF7JJ-L7J..JJ.L7-JJFF.F7F-..7J||.L|-JL|.-L.JJLJ|F7L77|LFLJF.J-7J-.J
# 7||7-FFFFL7.|JF7L.F.-.J77|.|.LLJJ|7-LJJF|-.J|.|F.LJFJ.7L..LF||.-FL|FFL|L.-7-7.L|F|LL.-|L-LJFLF|FL.J..L|-L|7LF-||-J-||L-7|J.|F-JF7..LF.7...L-J|.7F-77|LL|77F|F7F7JLL|7J..77L.L.L|J.F|J.|JJL-LJJ7FLLF-L.7.|7-JF.|.F-LL7LJ.--LL.L-JJ7--LF||JJFFL..7.JFFJJLJJ77.7FLLL.|LL||7L|--F-|-.J.FF|FLJ7F-7L...7|7F-..F77JF-|FF-7L-7J-F7L-..7FFJ.L7FF|.JFLL7J77FJ.|7L--7JF-.J||J|F|L.||LJ|J|7-LLL||7.JJLF||JFLF7LJ|L..J-|-L-..F|J|LJF-J|L-7|JF
# J.--7J|-L|JLL|7J.LLL7JFL.J7-|-J7F7.-L7777J-FJLF-7F--F|LFJJJ||JF7L7JLFF|7L7.--L7L-|.F||L.LJF.J7F.-|.JLL|J7..|J7F|FF-J|F-JL--J|.7-J77||.|F7.J|--..|L..JL7|JJ.7L.J.||-|F.FL|F7-.FFJF7-F|7F.F7F|J-77FLFF|7F7JLJLF--LJLFJ7|.||L|F.J|-7JJL.L7.|77FFJ77-F-LLLL7..77FL7LFJ|7-.J|L|JLF|7.LF.F-|.7FLL|F7J.--F7F7JL|7|FF|-||JJ..|J7F7J-.F|J|-JL.-7-L7L|--LFL-L|||FJ.-LFJ--LJ-J.FJJ.-|J.J-.FL7.|.77.JLJ|F.FFLF7J7LJ|-7|J||JL|F7JLJ..-F7|L7JJ
# .-.7|F|-|L.L7JL.F.LJ7.L-LLL|F|77JLL.77J7|-L||.7FF.77.|-F7L--7.7|FJ|||.-.L|L7...-JJ..JF77FJLFLJ..--F|.JL..LJ.-JLJJL-7||F--7F-J7.LJ.7L77LL-|-L-.-L-J--.JFF|77LLLFJ.|7-7-F-J|.L|-7-FJ..F|F7FF|.7|-L|.-F-L.J7L.F-F7|7LL.|-.|7|J-.FF|FF.J7|JF|FJ|.J7FJLF7|7|7L7-...-.||L7L..L7JFJFJ|L|7..F.FJ||7.77-|J7F.|--FLJL-J-FJJJ---FJF|-JL.J7|FFJF.FF.-FF.7J.JFFJ|F|7.LLF|J|7L..LFJLJ.7-.JL.JFFJ-F..J|-L|.-7F.|JL7-L7..J7|.-7LJJ|FLJJJ7.JLJFLF
# |--7..LJ.|7L-.7J.FL-LJ7|J|LJ-L.FJ7-LL-J.7FF.JL|L.J.7F|J777-FFL|J.-7-||FJFLFLLLL7F.LF--77.L7-J.|F|FJ7LFL7||777|F..L7|LJL-7||.7F7LJ7FFFJ7.LF.F-FF|||F.F.JJFFF.FJJ..L7JF|L-|.||-|77LFF7-JF|FF7FLFJ7J-||JL|J7JJJ.J77|.L-7J-F-J.FLL.-|J.7J-|.L-FLFJJL.LLJ-F|-F-J7.-.LLFJL7JL77LL.L.|FL7FJ77JLF|.|7-|JJ|7|---|7.-LJJ|F||-J7F-JJFL-|7|7F-FFFJF7J.F7FL7.J-|J|JF.J-||-LJ|L-LJ.J.F-LF7J|F.L7|F|-L-7|JJ|--J|FLJL-||--JF7-J.|FJ7FLJ7LFL|7L||
# -.J..|F|.FFL.-LJJL|--F--.|7|-7F-L-.JF--|FJ|LJFFLLJL|FF7LF.F-LLJ7..L7-FJ-J|.-F.---L7F-|7LF-J.|-|L|F|J|L-||-J-LL7J|7LL----JLJ|-.JL7LL|..LFJ||J7JFFL--||J7FL7.JF.7FL.L-F--|FJ-J7J-|J7.F|F..J.L.J|.F--7J7|J7FF7..LJ-.-|L.F|FL|J-J.J|FF-|7LF--.--FFJLJ||FJ7|7FLLJ|L--7L-7JF..F.--L|.F.F-F-|--F-F-L.FLF.F-LJ|L7J7JF|-7LJFLLF7FL..L||FFJ7..J-LFJ||.--|.F.LJ..F|F.-JJLF77F|.F77777|F-JL|L-.7J-7LFF.LF|-LLJ7.77F7|.-7-LLFJF|FJ7L7||J.J7J-
# |LF.F|.-7J7L-LFF7-FL-L7FJJF77-..F.J.FF.FJ|-LF.L-.-|LJ|-..LF|-LLF|JFJ.-L..7|-|7F|77FF-JL..J-7.7|7.-JJ.JL7-F7|7|.J7LJ-FFL7F--LJ||77JJ-LF|F||-J7.||FF.||FF7|.|L.FLF7L7.7-J||J-|-F-JFJJ7|J7...J|-F.FJLJ7LJLLL7.FJ-FLJ|7F----|7.77JJFF|7-.L7|.L7J.-.L-LFJL.J|L7-|L.L7.JLFL.7L-||-7--.7JJLJ-FF.|F-FJL7F|.J.|J7.F|F-.-FF-F7|J.7|7J7F..F-.J-.FL|.|F7|F|FF..LJFFLLJ||-F---JL|L|-..|-|-LJLJF7J-|||J-..-L7L7.L.J-7F-L|..J|7LJ--.LF.-LFL-.--
# """

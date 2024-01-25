import logging
from abc import ABC
from dataclasses import dataclass

from aoc import AOC
from aoc.problems import MultiLineProblem

octopi: dict[tuple[int, int], 'Octopus'] = {}


@dataclass
class Octopus:
    energy: int
    x: int
    y: int

    def check_flash(self) -> None:
        if self.energy <= 9:
            return
        # flash!
        self.energy = 0

        # boost neighbors that haven't flashed
        for i in -1, 0, 1:
            for j in -1, 0, 1:
                x, y = self.x + i, self.y + j
                if (x, y) not in octopi:
                    # skip edge lords
                    continue

                octopus = octopi[x, y]
                if not octopus.energy:
                    # skip already flashed
                    continue

                # boost neighbor
                octopus.energy += 1
                octopus.check_flash()


class _Problem(MultiLineProblem[int], ABC):
    def assignment(self, max_steps: int = None) -> list[int]:
        for y, line in enumerate(self.lines):
            for x, energy in enumerate(line):
                octopi[x, y] = Octopus(int(energy), x, y)

        flashes = []
        steps = 0
        while not max_steps or steps < max_steps:
            steps += 1
            size = len(self.lines[0])
            if AOC.debugging:
                for y in range(size):
                    logging.debug(' '.join(
                        f'{octopi[x, y].energy} ' if octopi[x, y].energy else '💩'
                        for x in range(size)
                    ))
                logging.debug('')

            for octopus in octopi.values():
                octopus.energy += 1
            for octopus in octopi.values():
                octopus.check_flash()

            step_flashes = len([o for o in octopi.values() if not o.energy])
            flashes.append(step_flashes)
            if step_flashes == len(octopi):
                break

        return flashes


class Problem1(_Problem):
    test_solution = 1656
    my_solution = 1749

    def solution(self) -> int:
        return sum(self.assignment(max_steps=100))


class Problem2(_Problem):
    test_solution = 195
    my_solution = 285

    def solution(self) -> int:
        return len(self.assignment())


TEST_INPUT = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

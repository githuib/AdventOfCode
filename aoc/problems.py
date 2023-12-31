import logging
import sys
import unicodedata
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, Generic, NamedTuple, Self, TypeVar

from more_itertools import strip
from parse import findall  # type: ignore[import-untyped]
from yachalk import chalk

from aoc import AOC, InputMode
from aoc.geo2d import E, Grid2
from aoc.geo3d import P3D
from aoc.utils import human_readable_duration, timed

T = TypeVar('T')


def strlen(s: str) -> int:
    return sum((2 if unicodedata.east_asian_width(c) == 'W' else 1) for c in s)


def solution_lines(my_solution: T, actual_solution: T) -> list[str]:
    mine: list[str] = my_solution.strip().splitlines() if isinstance(my_solution, str) else [str(my_solution)]
    actual: list[str] = [''] if (
        actual_solution is None
    ) else actual_solution.strip().splitlines() if (
        isinstance(actual_solution, str)
    ) else [str(actual_solution)]
    if len(mine) > 1:
        mine = [''] + mine
    if len(actual) > 1:
        actual = [''] + actual
    if actual == ['']:
        return ['Attempted solution... 👾'] + mine
    if mine == actual:
        return ['Correct solution! 🍻'] + mine
    return ['Wrong solution! 💀'] + ([f'{mine[0]} <- your answer', f'{actual[0]} <- right answer'] if (
        len(mine) == 1 and len(actual) == 1
    ) else ['', 'Your answer:'] + mine + ['', 'Right answer:'] + actual)


def duration_emoji(duration_str) -> str:
    if duration_str.endswith('minutes'):
        return '🦥'
    if duration_str.endswith('seconds'):
        return '🐢'
    if duration_str.endswith('ms'):
        return '🐇'
    return '🚀'


def var(test: T, puzzle: T) -> T:
    return test if AOC.input_mode == InputMode.TEST else puzzle


class NoSolutionFound(Exception):
    pass


class FatalError(Exception):
    def __init__(self, message: str):
        self.message = message


class Problem(ABC, Generic[T]):
    class Data(NamedTuple):
        year: int
        day: int
        part: int

    data: ClassVar[Data]

    test_solution: T | None = None
    my_solution: T | None = None

    line_count: int
    input: str
    corrected_input: str

    def __new__(cls: type['Self']) -> 'Self':
        # Read input into problem instance before its actual __init__() will be called.
        self: 'Self' = super().__new__(cls)
        if AOC.input_mode == InputMode.NONE:
            return self
        module = sys.modules[cls.__module__]
        try:
            if AOC.input_mode == InputMode.PUZZLE:
                with open(f'input/{cls.data.year}/{cls.data.day:02d}.txt', 'r', encoding='utf8') as input_file:
                    self.set_input(input_file.read())
            else:
                part_input = f'TEST_INPUT_{cls.data.part}'
                self.set_input(getattr(module, part_input if (part_input in dir(module)) else 'TEST_INPUT'))
        except (IOError, AttributeError):
            # fall back to legacy way of doing things with separate input files
            dir_name = Path(module.__file__ or '.').with_suffix('')
            file_name = 'test_input.txt' if AOC.input_mode == InputMode.TEST else 'input.txt'
            try:
                with open(dir_name / file_name, 'r', encoding='utf8') as input_file:
                    self.set_input(input_file.read())
            except IOError as exc:
                raise FatalError(f'Could not find {AOC.input_mode.value} input!') from exc
        return self

    def set_input(self, input_: str) -> None:
        self.input = input_
        self.corrected_input = input_.lstrip('\n').rstrip() + '\n'
        self.line_count = self.corrected_input.count('\n')
        self.process_input()

    @classmethod
    def solve(cls, year: int, day: int, part: int, input_mode: InputMode, debugging: bool = False) -> None:
        cls.data = cls.Data(year, day, part)
        AOC.setup(input_mode, debugging)
        try:
            problem, duration_init, _duration_init_str = timed(cls)
            solution, duration_solution, _duration_solution_str = timed(problem.solution)
        except NoSolutionFound:
            lines = ['No solution found!? 🤷‍️']
        except FatalError as exc:
            logging.fatal(exc.message)
            lines = ['The process died before a solution could be found. 💀‍️']
        else:
            duration_total = duration_init + duration_solution
            duration_str = human_readable_duration(duration_total)
            if solution is None:
                return
            given_solution = cls.test_solution if input_mode == InputMode.TEST else cls.my_solution
            lines = solution_lines(solution, given_solution)
            lines += ['', f'Solved in {duration_str} {duration_emoji(duration_str)}']
            # if debugging:
            #     lines += [
            #         '-----------------------',
            #         f'    init: {duration_init_str}',
            #         f'solution: {duration_solution_str}',
            #     ]
        width = max(strlen(line) for line in lines)
        logging.info(' ' * (width + 4))
        logging.info(' %s ', chalk.bg_hex('332')(' ' * (width + 2)))
        for line in lines:
            logging.info(' %s ', chalk.bg_hex('332')(f' {line} {' ' * (width - strlen(line))}'))
        logging.info(' %s ', chalk.bg_hex('332')(' ' * (width + 2)))
        logging.info(' ' * (width + 4))

    @abstractmethod
    def process_input(self) -> None:
        pass

    @abstractmethod
    def solution(self) -> T:
        pass


class OneLineProblem(Problem[T], ABC, Generic[T]):
    line: str

    def process_input(self) -> None:
        self.line = self.input.strip()


class MultiLineProblem(Problem[T], ABC, Generic[T]):
    lines: list[str]

    def process_input(self) -> None:
        self.lines = list(strip(self.corrected_input.splitlines(), lambda line: line == ''))


class _GridProblem(MultiLineProblem[T], ABC, Generic[E, T]):
    grid: Grid2[E]


class GridProblem(_GridProblem[str, T], ABC, Generic[T]):
    def process_input(self) -> None:
        super().process_input()
        self.grid = Grid2.from_lines(self.lines)


class NumberGridProblem(_GridProblem[int, T], ABC, Generic[T]):
    def process_input(self) -> None:
        super().process_input()
        self.grid = Grid2.from_lines(self.lines).converted(self.convert_element)

    def convert_element(self, element: str) -> int:
        return int(element)


R = TypeVar('R')


class ParsedProblem(Problem[T], ABC, Generic[R, T]):
    line_pattern: str = ''
    multi_line_pattern: str = ''
    # _regex_pattern: str | None
    # _regex_converters: list[Callable[[str], Any]] | None

    parsed_input: list[R]
    # parsed_regex: list[list]

    def process_input(self) -> None:
        if not self.line_pattern and not self.multi_line_pattern:
            raise TypeError('Either line_pattern or multi_line_pattern should be set.')
        prefix = '__parse_'
        module = sys.modules[self.__module__]
        extra_types = {
            f[len(prefix):]: getattr(module, f)
            for f in dir(module) if f.startswith(prefix)
        } | {
            'p3': P3D.from_str
        }
        self.parsed_input = [r.fixed for r in findall(
            self.multi_line_pattern or self.line_pattern + '\n',
            self.corrected_input,
            extra_types=extra_types,
        )]
        # elif self._regex_pattern:
        #     rc = self._regex_converters or []
        #     self.parsed_regex = [
        #         [(rc[n](g) if n < len(rc) else g) for n, g in enumerate(groups)]
        #         for groups in re.findall(self._regex_pattern, self.corrected_input)
        #     ]

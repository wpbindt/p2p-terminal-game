import sys
import termios
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Iterator, Generic

from game import CommandType
from termios_io.termios_input_reader import TermiosInputReader
from termios_io.termios_output import TermiosOutput


@dataclass(frozen=True)
class TermiosIO(Generic[CommandType]):
    input_reader: TermiosInputReader
    output: TermiosOutput


@contextmanager
def create_termios_io(
    command_parser: Callable[[str], CommandType],
) -> Iterator[TermiosIO]:
    stdin = sys.stdin.fileno()
    old = termios.tcgetattr(stdin)

    new = termios.tcgetattr(stdin)
    new[3] = new[3] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(stdin, termios.TCSAFLUSH, new)

    sys.stdout.write('\033[2J')
    sys.stdout.flush()

    yield TermiosIO(TermiosInputReader(command_parser), TermiosOutput())

    termios.tcsetattr(stdin, termios.TCSAFLUSH, old)

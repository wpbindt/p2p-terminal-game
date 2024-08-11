import sys
import termios
from contextlib import contextmanager
from typing import Callable, Iterator

from game import CommandType
from termios_io.termios_input_reader import TermiosInputReader
from termios_io.termios_output import TermiosOutput


@contextmanager
def create_termios_io(
    command_parser: Callable[[str], CommandType],
) -> Iterator[tuple[TermiosInputReader, TermiosOutput]]:
    stdin = sys.stdin.fileno()
    old = termios.tcgetattr(stdin)

    new = termios.tcgetattr(stdin)
    new[3] = new[3] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(stdin, termios.TCSAFLUSH, new)

    sys.stdout.write('\033[2J')
    sys.stdout.flush()

    yield TermiosInputReader(command_parser), TermiosOutput()

    termios.tcsetattr(stdin, termios.TCSAFLUSH, old)

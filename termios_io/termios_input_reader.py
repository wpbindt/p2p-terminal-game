import sys
import termios
from typing import Callable, Generic

from game import CommandType
from try_something import InputReader, Command


class TermiosInputReader(InputReader[CommandType], Generic[CommandType]):
    def __init__(
        self,
        command_parser: Callable[[str], CommandType],
    ) -> None:
        self._command_parser = command_parser
        stdin = sys.stdin.fileno()
        self._old = termios.tcgetattr(stdin)

    def __enter__(self):
        stdin = sys.stdin.fileno()
        new = termios.tcgetattr(stdin)
        new[3] = new[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(stdin, termios.TCSAFLUSH, new)

    def __exit__(self, exc_type, exc_val, exc_tb):
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, self._old)

    def get_input(self) -> Command:
        return self._command_parser(
            sys.stdin.buffer.read(1).decode()
        )

import sys
from typing import Callable, Generic

from game import CommandType
from try_something import InputReader, Command


class TermiosInputReader(InputReader[CommandType], Generic[CommandType]):
    def __init__(
        self,
        command_parser: Callable[[str], CommandType],
    ) -> None:
        self._command_parser = command_parser

    def get_input(self) -> Command:
        return self._command_parser(
            sys.stdin.buffer.read(1).decode()
        )

import sys
from dataclasses import dataclass

from try_something import Output


@dataclass(frozen=True)
class TermiosSymbol:
    x: int
    y: int
    to_draw: str

    def draw(self) -> None:
        sys.stdout.write(f'\033[{self.x};{self.y}H')
        sys.stdout.write(self.to_draw)
        sys.stdout.flush()


@dataclass(frozen=True)
class TermiosDrawInstruction:
    symbols: list[TermiosSymbol]

    def draw(self) -> None:
        for symbol in self.symbols:
            symbol.draw()


class TermiosOutput(Output[TermiosDrawInstruction]):
    def __init__(self):
        sys.stdout.write('\033[2J')
        sys.stdout.flush()

    def draw(self, draw_instruction: TermiosDrawInstruction) -> None:
        draw_instruction.draw()

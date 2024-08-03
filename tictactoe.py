from __future__ import annotations

from typing import Iterable, Generator
from dataclasses import dataclass

from game import Game, CommandType, run_game


@dataclass(frozen=True)
class Naught:
    def to_string(self) -> str:
        return 'o'


@dataclass(frozen=True)
class Cross:
    def to_string(self) -> str:
        return 'x'


@dataclass(frozen=True)
class Empty:
    def to_string(self) -> str:
        return '.'


@dataclass(frozen=True)
class PlaceTile:
    tile: Naught | Cross
    x: int
    y: int


def parse_tic_tac_toe_command(raw: str) -> TicTacToeCommand:
    return PlaceTile(
        x=int(raw[0]),
        y=int(raw[1]),
        tile=Cross() if raw[2] == 'x' else Naught(),
    )


TicTacToeCommand = PlaceTile


Tile = Naught | Cross | Empty


class TicTacToeBoard(Game):
    def __init__(self) -> None:
        self._board: list[list[Tile]] = [[Empty() for _ in range(3)] for _ in range(3)]
        self._winner = None

    @property
    def _rows(self) -> Iterable[list[Tile]]:
        for r in range(len(self._board)):
            yield [
                self._board[x][r]
                for x in range(len(self._board))
            ]

    @property
    def _columns(self) -> Iterable[list[Tile]]:
        yield from self._board

    @property
    def _diagonals(self) -> Iterable[list[Tile]]:
        yield [self._board[x][x] for x in range(len(self._board))]
        yield [self._board[2 - x][x] for x in range(len(self._board))]

    @property
    def _triples(self) -> Iterable[tuple[Tile, Tile, Tile]]:
        yield from self._columns
        yield from self._rows
        yield from self._diagonals

    def determine_winner(self) -> Naught | Cross | None:
        if self._winner is not None:
            return self._winner
        for triple in self._triples:
            triple_winner = self._determine_triple_winner(triple)
            if isinstance(triple_winner, Empty):
                continue
            self._winner = triple_winner
            return triple_winner

        return None

    def mark_tile(self, command: TicTacToeCommand) -> None:
        if self._winner is not None:
            return
        self._board[command.x][command.y] = command.tile

    def _determine_triple_winner(self, triple: tuple[Tile, Tile, Tile]) -> Tile:
        if len(set(triple)) == 1:
            return next(iter(triple))
        return Empty()

    def __str__(self) -> str:
        lines = [
            ''.join(tile.to_string() for tile in row) 
            for row in self._rows
        ]
        if self._winner is not None:
            lines.append(f'\n{self._winner.to_string()} wins!')

        return '\n'.join(lines)

    def main_loop(self) -> Generator[str, CommandType, None]:
        while True:
            command = yield str(self)
            self.mark_tile(command)
            self.determine_winner()


def print_board(board: str) -> None:
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(board)


if __name__ == '__main__':
    run_game(
        game=TicTacToeBoard(),
        print_game=print_board,
        command_parser=TicTacToeCommand.parse,
    )

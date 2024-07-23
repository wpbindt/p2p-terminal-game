from typing import Iterable
from dataclasses import dataclass

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



Tile = Naught | Cross | Empty


class TicTacToeBoard:
    def __init__(self) -> None:
        self._board = [[Empty() for _ in range(3)] for _ in range(3)]

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
    def _triples(self) -> Iterable[list[Tile]]:
        yield from self._columns
        yield from self._rows
        yield from self._diagonals

    def determine_winner(self) -> Naught | Cross | None:
        for triple in self._triples:
            triple_winner = self._determine_triple_winner(triple)
            if isinstance(triple_winner, Empty):
                continue
            return triple_winner

        return None

    def mark_tile(self, x: int, y: int, tile: Naught | Cross) -> None:
        self._board[x][y] = tile

    def _determine_triple_winner(self, triple: tuple[Tile, Tile, Tile]) -> Tile:
        if len(set(triple)) == 1:
            return next(iter(triple))
        return Empty()

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(tile.to_string() for tile in row) 
            for row in self._rows
        )


def test_determine_winner_on_empty_board():
    board = TicTacToeBoard()

    assert board.determine_winner() is None


def test_determine_winner_when_top_row_is_naughts() -> None:
    board = TicTacToeBoard()

    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Naught())
    board.mark_tile(2, 0, Naught())

    assert board.determine_winner() == Naught()

    
def test_determine_winner_when_top_row_is_not_naughts_two_tile() -> None:
    board = TicTacToeBoard()

    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Naught())

    assert board.determine_winner() is None


def test_determine_winner_when_top_row_is_not_naughts() -> None:
    board = TicTacToeBoard()

    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Naught())
    board.mark_tile(0, 1, Naught())

    assert board.determine_winner() is None


def test_determine_winner_when_first_column_is_naughts() -> None:
    board = TicTacToeBoard()

    board.mark_tile(0, 1, Naught())
    board.mark_tile(0, 2, Naught())
    board.mark_tile(0, 0, Naught())

    assert board.determine_winner() == Naught()


def test_determine_winner_for_diagonal_crosses() -> None:
    board = TicTacToeBoard()

    board.mark_tile(0, 0, Cross())
    board.mark_tile(2, 2, Cross())
    board.mark_tile(1, 1, Cross())

    assert board.determine_winner() == Cross()


def test_determine_winner_for_diagonal() -> None:
    board = TicTacToeBoard()

    board.mark_tile(0, 0, Naught())
    board.mark_tile(2, 2, Naught())
    board.mark_tile(1, 1, Naught())

    assert board.determine_winner() == Naught()

def test_determine_winner_for_anti_diagonal() -> None:
    board = TicTacToeBoard()

    board.mark_tile(0, 2, Naught())
    board.mark_tile(2, 0, Naught())
    board.mark_tile(1, 1, Naught())

    assert board.determine_winner() == Naught()


def test_that_the_board_prints_nicely() -> None:
    board = TicTacToeBoard()
    assert str(board) == '\n'.join('...')


def test_that_the_board_prints_nicely() -> None:
    board = TicTacToeBoard()
    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Cross())
    board.mark_tile(1, 1, Naught())
    assert str(board) == 'ox.\n.o.\n...'

def print_board(board: TicTacToeBoard) -> None:
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    print(board)


def main_game_loop():
    board = TicTacToeBoard()
    print('\n')
    print('\n')
    while True:
        print_board(board)
        winner = board.determine_winner()
        if isinstance(winner, (Naught, Cross)):
            print(f'{winner.to_string()} wins!')
            exit(0)
        command = input()  # xy(tile)
        tile = Cross() if command[2] == 'x' else Naught()
        board.mark_tile(int(command[0]), int(command[1]), tile)


if __name__ == '__main__':
    main_game_loop()


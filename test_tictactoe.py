from tictactoe import TicTacToeBoard, Naught, Cross, parse_tic_tac_toe_command, PlaceTile, MovePlayer, Direction, \
    PutTile


def test_determine_winner_on_empty_board():
    board = TestAdapter(TicTacToeBoard())

    assert board.determine_winner() is None


class TestAdapter:
    def __init__(self, board: TicTacToeBoard) -> None:
        self._board = board
        self._main_loop = board.main_loop()
        next(self._main_loop)

    def mark_tile(self, x: int, y: int, tile: Naught | Cross) -> None:
        for _ in range(x):
            self._main_loop.send(MovePlayer(direction=Direction.RIGHT))
        for _ in range(y):
            self._main_loop.send(MovePlayer(direction=Direction.DOWN))

        self._main_loop.send(PutTile(tile=tile))

        for _ in range(x):
            self._main_loop.send(MovePlayer(direction=Direction.LEFT))
        for _ in range(y):
            self._main_loop.send(MovePlayer(direction=Direction.UP))

    def determine_winner(self) -> Naught | Cross | None:
        return self._board.determine_winner()

    def __str__(self) -> str:
        return str(self._board)


def test_determine_winner_when_top_row_is_naughts() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Naught())
    board.mark_tile(2, 0, Naught())

    assert board.determine_winner() == Naught()


def test_no_more_moves_after_winner_determined() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Naught())
    board.mark_tile(2, 0, Naught())

    before_extra_move = str(board)
    board.mark_tile(2, 1, Naught())
    after_extra_move = str(board)

    assert before_extra_move == after_extra_move


def test_determine_winner_when_top_row_is_not_naughts_two_tile() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Naught())

    assert board.determine_winner() is None


def test_determine_winner_when_top_row_is_not_naughts() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Naught())
    board.mark_tile(0, 1, Naught())

    assert board.determine_winner() is None


def test_determine_winner_when_first_column_is_naughts() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 1, Naught())
    board.mark_tile(0, 2, Naught())
    board.mark_tile(0, 0, Naught())

    assert board.determine_winner() == Naught()


def test_determine_winner_for_diagonal_crosses() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 0, Cross())
    board.mark_tile(2, 2, Cross())
    board.mark_tile(1, 1, Cross())

    assert board.determine_winner() == Cross()


def test_determine_winner_for_diagonal() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 0, Naught())
    board.mark_tile(2, 2, Naught())
    board.mark_tile(1, 1, Naught())

    assert board.determine_winner() == Naught()


def test_determine_winner_for_anti_diagonal() -> None:
    board = TestAdapter(TicTacToeBoard())

    board.mark_tile(0, 2, Naught())
    board.mark_tile(2, 0, Naught())
    board.mark_tile(1, 1, Naught())

    assert board.determine_winner() == Naught()


def test_that_the_board_prints_nicely_when_empty() -> None:
    board = TestAdapter(TicTacToeBoard())
    assert str(board) == '\n'.join(3 * ['...'])


def test_that_the_board_prints_nicely() -> None:
    board = TestAdapter(TicTacToeBoard())
    board.mark_tile(0, 0, Naught())
    board.mark_tile(1, 0, Cross())
    board.mark_tile(1, 1, Naught())
    assert str(board) == 'ox.\n.o.\n...'


def test_that_the_board_prints_nicely_when_a_winner_determined() -> None:
    board = TestAdapter(TicTacToeBoard())
    board.mark_tile(1, 0, Naught())
    board.mark_tile(1, 2, Naught())
    board.mark_tile(1, 1, Naught())
    assert 'o wins!' in str(board)


def test_parse_command() -> None:
    assert parse_tic_tac_toe_command('12x') == PlaceTile(tile=Cross(), x=1, y=2)

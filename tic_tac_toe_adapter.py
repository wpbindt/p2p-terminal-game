from termios_output import TermiosDrawInstruction, TermiosSymbol
from tictactoe import TicTacToeCommand, TicTacToeBoard
from try_something import Game


class TicTacToeAdapter(Game[TicTacToeCommand, TermiosDrawInstruction]):
    def __init__(self, board: TicTacToeBoard) -> None:
        self._loop = board.main_loop()
        self._current_presentation = next(self._loop)

    def handle_command(self, command: TicTacToeCommand) -> TermiosDrawInstruction:
        self._current_presentation = self._loop.send(command)
        return self._convert_to_draw_instruction(self._current_presentation)

    def draw_full_screen(self) -> TermiosDrawInstruction:
        return self._convert_to_draw_instruction(self._current_presentation)

    def _convert_to_draw_instruction(self, presentation: str) -> TermiosDrawInstruction:
        lines = presentation.split('\n')
        symbols: list[TermiosSymbol] = []
        for x, line in enumerate(lines, 1):
            for y, character in enumerate(line, 1):
                symbols.append(
                    TermiosSymbol(
                        x=x,
                        y=y,
                        to_draw=character,
                    )
                )
        return TermiosDrawInstruction(symbols)

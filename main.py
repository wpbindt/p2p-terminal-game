from queue import Queue

from termios_input_reader import TermiosInputReader
from tictactoe import parse_termios_command, TicTacToeBoard
from try_something import CommandQueue, Controller, TicTacToeAdapter, GameRunner, TerminalOutput


if __name__ == '__main__':
    command_queue = CommandQueue(commands=Queue(maxsize=100))
    reader = TermiosInputReader(
        command_parser=parse_termios_command
    )
    controller = Controller(
        input_reader=reader,
        command_queue=command_queue,
    )
    game = TicTacToeAdapter(TicTacToeBoard())
    game_runner = GameRunner(
        command_queue=command_queue,
        game=game,
    )
    output = TerminalOutput()
    game_runner.subscribe(output)
    game_runner.add_controller(controller)
    with reader:
        game_runner.run()
from queue import Queue

from termios_io.factory import create_termios_io
from tic_tac_toe_adapter import TicTacToeAdapter
from tictactoe import parse_termios_command, TicTacToeBoard
from try_something import CommandQueue, Controller, GameRunner

if __name__ == '__main__':
    command_queue = CommandQueue(commands=Queue(maxsize=100))
    game = TicTacToeAdapter(TicTacToeBoard())
    game_runner = GameRunner(
        command_queue=command_queue,
        game=game,
    )
    with create_termios_io(command_parser=parse_termios_command) as termios_io:
        controller = Controller(
            input_reader=termios_io.input_reader,
            command_queue=command_queue,
        )
        game_runner.subscribe(termios_io.output)
        game_runner.add_controller(controller)
        game_runner.run()

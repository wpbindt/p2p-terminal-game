import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import Queue
from typing import Callable, NoReturn

from tictactoe import TicTacToeBoard, parse_tic_tac_toe_command


class Command:
    pass


@dataclass(frozen=True)
class CommandQueue:
    commands: Queue[Command]

    def put(self, command: Command) -> None:
        self.commands.put_nowait(command)

    def get(self) -> Command:
        return self.commands.get(block=True)


class InputReader(ABC):
    @abstractmethod
    def get_input(self) -> Command:
        pass


@dataclass(frozen=True)
class LineInputReader(InputReader):
    command_parser: Callable[[str], Command]

    def get_input(self) -> Command:
        raw = input()
        return self.command_parser(raw)


@dataclass(frozen=True)
class Controller:
    command_queue: CommandQueue
    input_reader: InputReader

    def run(self) -> None:
        while True:
            command = self.input_reader.get_input()
            self.command_queue.put(command)


DrawInstruction = str


class Output(ABC):
    @abstractmethod
    def draw(self, draw_instruction: DrawInstruction) -> None:
        pass


class TerminalOutput(Output):
    def draw(self, draw_instruction: DrawInstruction) -> None:
        print(draw_instruction)


class Game(ABC):
    @abstractmethod
    def handle_command(self, command: Command) -> DrawInstruction:
        pass

    @abstractmethod
    def draw_full_screen(self) -> DrawInstruction:
        pass


class TicTacToeAdapter(Game):
    def __init__(self, board: TicTacToeBoard) -> None:
        self._loop = board.main_loop()
        self._current_presentation = next(self._loop)

    def handle_command(self, command: Command) -> DrawInstruction:
        self._current_presentation = self._loop.send(command)
        return self._current_presentation

    def draw_full_screen(self) -> DrawInstruction:
        return self._current_presentation


@dataclass(frozen=True)
class GameRunner:
    command_queue: CommandQueue
    game: Game
    controller_threads: list[threading.Thread] = field(default_factory=list)
    subscribers: list[Output] = field(default_factory=list)

    def run(self) -> NoReturn:
        while True:
            command = self.command_queue.get()
            draw_instruction = self.game.handle_command(command)
            for subscriber in self.subscribers:
                subscriber.draw(draw_instruction)

    def subscribe(self, subscriber: Output) -> None:
        self.subscribers.append(subscriber)
        subscriber.draw(self.game.draw_full_screen())

    def add_controller(self, controller: Controller) -> None:
        thread = threading.Thread(target=controller.run)
        thread.start()
        self.controller_threads.append(thread)


if __name__ == '__main__':
    command_queue = CommandQueue(commands=Queue(maxsize=100))
    reader = LineInputReader(
        command_parser=parse_tic_tac_toe_command
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
    game_runner.run()

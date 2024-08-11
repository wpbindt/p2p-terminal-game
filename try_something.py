import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from queue import Queue
from typing import Callable, NoReturn, Generic, TypeVar

from game import CommandType


class Command:
    pass


@dataclass(frozen=True)
class CommandQueue(Generic[CommandType]):
    commands: Queue[CommandType]

    def put(self, command: CommandType) -> None:
        self.commands.put_nowait(command)

    def get(self) -> CommandType:
        return self.commands.get(block=True)


class InputReader(ABC, Generic[CommandType]):
    @abstractmethod
    def get_input(self) -> CommandType:
        pass


@dataclass(frozen=True)
class LineInputReader(InputReader[CommandType], Generic[CommandType]):
    command_parser: Callable[[str], CommandType]

    def get_input(self) -> CommandType:
        raw = input()
        return self.command_parser(raw)


@dataclass(frozen=True)
class Controller(Generic[CommandType]):
    command_queue: CommandQueue[CommandType]
    input_reader: InputReader[CommandType]

    def run(self) -> None:
        while True:
            command = self.input_reader.get_input()
            self.command_queue.put(command)


DrawInstructionType = TypeVar('DrawInstructionType')
DrawInstruction = str


class Output(ABC, Generic[DrawInstructionType]):
    @abstractmethod
    def draw(self, draw_instruction: DrawInstructionType) -> None:
        pass


class TerminalOutput(Output):
    def draw(self, draw_instruction: DrawInstructionType) -> None:
        print(draw_instruction)


class Game(ABC, Generic[CommandType, DrawInstructionType]):
    @abstractmethod
    def handle_command(self, command: CommandType) -> DrawInstructionType:
        pass

    @abstractmethod
    def draw_full_screen(self) -> DrawInstructionType:
        pass


@dataclass(frozen=True)
class GameRunner(Generic[CommandType, DrawInstructionType]):
    command_queue: CommandQueue[CommandType]
    game: Game[CommandType, DrawInstructionType]
    controller_threads: list[threading.Thread] = field(default_factory=list)
    subscribers: list[Output[DrawInstructionType]] = field(default_factory=list)

    def run(self) -> NoReturn:
        while True:
            command = self.command_queue.get()
            draw_instruction = self.game.handle_command(command)
            for subscriber in self.subscribers:
                subscriber.draw(draw_instruction)

    def subscribe(self, subscriber: Output[DrawInstructionType]) -> None:
        self.subscribers.append(subscriber)
        subscriber.draw(self.game.draw_full_screen())

    def add_controller(self, controller: Controller[CommandType]) -> None:
        thread = threading.Thread(target=controller.run)
        thread.start()
        self.controller_threads.append(thread)

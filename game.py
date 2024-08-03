from abc import ABC, abstractmethod
from typing import Generic, Generator, TypeVar, NoReturn, Callable

CommandType = TypeVar('CommandType')


class Game(ABC, Generic[CommandType]):
    @abstractmethod
    def main_loop(self) -> Generator[str, CommandType, None]:
        pass


GameType = TypeVar('GameType', bound=Game)


def run_game(
    print_game: Callable[[str], None],
    game: Game[CommandType],
    command_parser: Callable[[str], CommandType],
) -> NoReturn:
    main_loop = game.main_loop()
    presentation = next(main_loop)
    while True:
        print_game(presentation)
        presentation = main_loop.send(
            command_parser(
                input()
            )
        )

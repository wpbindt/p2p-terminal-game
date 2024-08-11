from typing import Callable

import requests

from try_something import Output, DrawInstructionType


class HttpOutput(Output):
    def __init__(
        self,
        url: str,
        serialize_draw_instruction: Callable[[DrawInstructionType], list],
    ) -> None:
        self._url = url
        self._serialize_draw_instruction = serialize_draw_instruction

    def draw(self, draw_instruction: DrawInstructionType) -> None:
        response = requests.post(self._url, json={'data': self._serialize_draw_instruction(draw_instruction)})
        response.raise_for_status()

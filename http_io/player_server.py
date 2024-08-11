from typing import Callable
import logging

from flask import Flask, request

from http_io.serialization import deserialize_draw_instruction
from termios_io.factory import create_termios_io
from termios_io.termios_output import TermiosOutput, TermiosDrawInstruction


def create_server(
    draw_instruction_deserializer: Callable[[list], TermiosDrawInstruction],
    termios_output: TermiosOutput,
) -> Flask:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app = Flask(__name__)

    @app.route('/draw', methods=['POST'])
    def draw():
        draw_instruction = draw_instruction_deserializer(request.json['data'])
        termios_output.draw(draw_instruction)
        return 'ok'

    return app


if __name__ == '__main__':
    with create_termios_io(command_parser=lambda x: x) as termios_io:
        app = create_server(
            termios_output=termios_io.output,
            draw_instruction_deserializer=deserialize_draw_instruction,
        )
        app.run('0.0.0.0', port=8080)

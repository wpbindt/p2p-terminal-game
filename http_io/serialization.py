from termios_io.termios_output import TermiosDrawInstruction, TermiosSymbol


def serialize_draw_instruction(draw_instruction: TermiosDrawInstruction) -> list[dict[str, str | int]]:
    return [
        serialize_symbol(symbol=symbol)
        for symbol in draw_instruction.symbols
    ]


def serialize_symbol(symbol: TermiosSymbol) -> dict[str, str | int]:
    return {
        'x': symbol.x,
        'y': symbol.y,
        'to_draw': symbol.to_draw,
    }


def deserialize_symbol(symbol: dict[str, int | str]) -> TermiosSymbol:
    return TermiosSymbol(
        x=symbol['x'],
        y=symbol['y'],
        to_draw=symbol['to_draw'],
    )


def deserialize_draw_instruction(raw: list[dict[str, int | str]]) -> TermiosDrawInstruction:
    return TermiosDrawInstruction(
        symbols=[
            deserialize_symbol(symbol)
            for symbol in raw
        ]
    )

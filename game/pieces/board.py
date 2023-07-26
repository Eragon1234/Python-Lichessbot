from typing import Protocol

from game.pieces.color import Color


class Board(Protocol):
    def color_at(self, position: tuple[int, int]) -> Color:
        pass

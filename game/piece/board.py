from typing import Protocol

from game.coordinate import Coordinate
from game.piece.color import Color


class Board(Protocol):
    def color_at(self, position: Coordinate) -> Color:
        pass

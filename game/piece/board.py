from typing import Protocol

from game.coordinate import Coordinate
from game.piece.color import Color
from game.piece.piece_type import PieceType


class Board(Protocol):
    def color_at(self, position: Coordinate) -> Color:
        pass

    def is_type(self, i: int, t: PieceType):
        pass

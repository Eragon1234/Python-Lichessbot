from typing import Protocol

from game.coordinate import Coordinate
from game.piece.piece_type import PieceType


class Board(Protocol):
    def is_type(self, i: int | Coordinate, t: PieceType):
        pass

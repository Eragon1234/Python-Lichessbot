from typing import Protocol, Optional

from game.coordinate import Coordinate
from game.piece.piece_type import PieceType


class MoveFactory(Protocol):
    def __call__(self, piece_type: PieceType,
                 start: Coordinate, end: Coordinate,
                 *, castling: bool = False,
                 promote_to: Optional[PieceType] = None):
        ...

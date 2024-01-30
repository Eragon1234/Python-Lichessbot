from typing import Protocol, Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.piece_type import PieceType


class Board(Protocol):
    en_passant: Optional[Coordinate]
    castling_rights: CastlingRights

    def is_type(self, i: Coordinate, t: PieceType):
        pass

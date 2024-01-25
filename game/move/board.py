from typing import Protocol, Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.color import Color
from game.piece.piece_type import PieceType


class Board(Protocol):
    def __getitem__(self, item: Coordinate) -> PieceType:
        ...

    def __setitem__(self, key: Coordinate, value: PieceType):
        ...

    def is_type(self, i: int, t: PieceType):
        ...

    def do_move(self, start_field: Coordinate,
                target_field: Coordinate) -> PieceType:
        ...

    def pop(self, field: Coordinate) -> PieceType:
        ...

    en_passant: Optional[Coordinate]

    castling_rights: CastlingRights

    turn: Color

    halfmove_clock: int

    fullmove_number: int

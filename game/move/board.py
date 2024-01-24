from typing import Protocol, Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.color import Color
from game.piece.piece_type import PieceType


class Piece(Protocol):
    color: Color
    type: PieceType


class Board(Protocol):
    def __getitem__(self, item: Coordinate) -> Piece:
        ...

    def __setitem__(self, key: Coordinate, value: Piece):
        ...

    def is_type(self, i: int, t: PieceType):
        ...

    def do_move(self, start_field: Coordinate,
                target_field: Coordinate) -> Piece:
        ...

    def pop(self, field: Coordinate) -> Piece:
        ...

    def clone(self) -> 'Board':
        ...

    en_passant: Optional[Coordinate]

    castling_rights: CastlingRights

    turn: Color

    halfmove_clock: int

    fullmove_number: int

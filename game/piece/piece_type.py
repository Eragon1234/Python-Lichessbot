from enum import Flag, auto
from functools import cached_property

from game.piece.color import Color


class PieceType(Flag):
    PAWN = auto()
    ROOK = auto()
    KNIGHT = auto()
    BISHOP = auto()
    QUEEN = auto()
    KING = auto()

    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()

    COLORS = WHITE | BLACK

    @staticmethod
    def from_fen(f: str) -> 'PieceType':
        return _piece_type_from_fen(f)

    def fen(self) -> str:
        return _fen_from_piece_type(self)

    @cached_property
    def type(self) -> 'PieceType':
        return self & ~PieceType.COLORS

    @cached_property
    def color(self) -> Color:
        if PieceType.WHITE in self:
            return Color.WHITE

        if PieceType.BLACK in self:
            return Color.BLACK

        return Color.EMPTY

    @cached_property
    def piece_value(self) -> int:
        return _value_from_piece_type(self.type)

    @cached_property
    def enemy(self) -> 'PieceType':
        if PieceType.WHITE in self:
            return PieceType.BLACK
        if PieceType.BLACK in self:
            return PieceType.WHITE
        return PieceType.EMPTY


_fen_to_piece_map = {
    'p': PieceType.PAWN,
    'r': PieceType.ROOK,
    'n': PieceType.KNIGHT,
    'b': PieceType.BISHOP,
    'q': PieceType.QUEEN,
    'k': PieceType.KING
}


def _piece_type_from_fen(fen: str) -> PieceType:
    color = PieceType.WHITE if fen.isupper() else PieceType.BLACK
    fen = fen.lower()

    t = _fen_to_piece_map[fen]
    t |= color
    return t


_piece_to_fen_map = {v: k for k, v in _fen_to_piece_map.items()}


def _fen_from_piece_type(piece_type: PieceType) -> str:
    if PieceType.WHITE in piece_type:
        return _piece_to_fen_map[piece_type.type].upper()

    return _piece_to_fen_map[piece_type.type]


_VALUES = {
    PieceType.PAWN: 1,
    PieceType.KNIGHT: 3,
    PieceType.BISHOP: 3,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 9,
    PieceType.KING: 9999,
    PieceType.EMPTY: 0
}


def _value_from_piece_type(piece_type: PieceType) -> int:
    return _VALUES[piece_type]

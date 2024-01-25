from enum import Flag, auto

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
        # color = PieceType.WHITE if f.isupper() else PieceType.BLACK
        f = f.lower()

        piece_map = {
            'p': PieceType.PAWN,
            'r': PieceType.ROOK,
            'n': PieceType.KNIGHT,
            'b': PieceType.BISHOP,
            'q': PieceType.QUEEN,
            'k': PieceType.KING
        }

        t = piece_map[f]
        return t

    def fen(self) -> str:
        piece_map = {
            PieceType.PAWN: 'p',
            PieceType.ROOK: 'r',
            PieceType.KNIGHT: 'n',
            PieceType.BISHOP: 'b',
            PieceType.QUEEN: 'q',
            PieceType.KING: 'k',
        }
        return piece_map[self]

    def get_type(self) -> 'PieceType':
        return self & ~PieceType.COLORS

    def to_color(self) -> Color:
        if PieceType.WHITE in self:
            return Color.WHITE

        if PieceType.BLACK in self:
            return Color.BLACK

        return Color.EMPTY

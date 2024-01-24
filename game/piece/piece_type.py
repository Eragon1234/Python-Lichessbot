from enum import Flag, auto


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

    def get_type(self) -> 'PieceType':
        return self & (
                PieceType.PAWN | PieceType.ROOK | PieceType.KNIGHT | PieceType.BISHOP | PieceType.QUEEN | PieceType.KING | PieceType.EMPTY)

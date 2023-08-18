from enum import Flag, auto


class CastlingRights(Flag):
    """
    Castling rights.
    """
    NONE = 0
    WHITE_KING = auto()
    WHITE_QUEEN = auto()
    BLACK_KING = auto()
    BLACK_QUEEN = auto()

    WHITE = WHITE_KING | WHITE_QUEEN
    BLACK = BLACK_KING | BLACK_QUEEN

    KING = WHITE_KING | BLACK_KING
    QUEEN = WHITE_QUEEN | BLACK_QUEEN

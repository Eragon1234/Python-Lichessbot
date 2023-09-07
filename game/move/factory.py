from functools import cache
from typing import Optional

from game.coordinate import Coordinate
from game.move import Move, RookMove, CastleMove, KingMove, PawnMove, PawnPromotion, NormalMove
from game.piece.piece_type import PieceType


@cache
def move_factory(piece_type: PieceType, start: Coordinate,
                 end: Coordinate, *, castling: bool = False,
                 promote_to: Optional[PieceType] = None) -> Move:
    """
    Factory function for creating a move.

    Args:
        piece_type: The type of the piece that is being moved.
        start: The starting coordinate of the move.
        end: The ending coordinate of the move.
        castling: Whether the move is a castling move.
        promote_to: The type to promote to if the move is a pawn promotion.

    Returns:
        Move: The corresponding move object based on the given parameters.
    """
    if piece_type is PieceType.ROOK:
        return RookMove(start, end)
    elif piece_type is PieceType.KING:
        if castling:
            return CastleMove(start, end)
        return KingMove(start, end)
    elif piece_type is PieceType.PAWN:
        if promote_to is None:
            return PawnMove(start, end)
        return PawnPromotion(start, end, promote_to)
    else:
        return NormalMove(start, end)

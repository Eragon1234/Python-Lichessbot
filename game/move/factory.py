from typing import Optional

from game.coordinate import Coordinate
from game.move import Move, RookMove, CastleMove, KingMove, PawnMove, PawnPromotion, NormalMove
from game.piece.piece_type import PieceType


def move_factory(piece_type: PieceType, start: Coordinate,
                 end: Coordinate, *, castling: bool = False,
                 promote_to: Optional[PieceType] = None) -> Move:
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

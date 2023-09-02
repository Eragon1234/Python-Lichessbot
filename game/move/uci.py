from game.coordinate import Coordinate
from game.move import Move, PawnPromotion, PawnMove, NormalMove, RookMove, KingMove, CastleMove
from game.move.board import Board
from game.piece.piece_type import PieceType


def move_from_uci(board: Board, uci: str) -> Move:
    """
    Converts a UCI string to a Move object.
    """
    if len(uci) == 5:
        return PawnPromotion.from_uci(uci)

    start_field = Coordinate.from_uci(uci[:2])
    target_field = Coordinate.from_uci(uci[2:4])
    moving_piece = board[start_field]

    if moving_piece.type is PieceType.PAWN:
        return PawnMove(start_field, target_field)
    elif moving_piece.type is PieceType.ROOK:
        return RookMove(start_field, target_field)
    elif moving_piece.type is PieceType.KING:
        if is_castle(start_field, target_field):
            return CastleMove(start_field, target_field)
        return KingMove(start_field, target_field)

    return NormalMove(start_field, target_field)


def is_castle(start: Coordinate, end: Coordinate) -> bool:
    """
    Checks if the move is a castle move.
    Expects the move to be a king move.
    """
    return abs(start.x - end.x) == 2

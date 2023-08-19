from game.coordinate import Coordinate
from game.move import Move, PawnPromotion, PawnMove, NormalMove, RookMove, KingMove, CastleMove
from game.move._chessboard import _ChessBoard
from game.piece.piece_type import PieceType


def move_from_uci(board: _ChessBoard, uci: str) -> Move:
    """
    Converts a UCI string to a Move object.
    """
    if len(uci) == 5:
        return PawnPromotion.from_uci(uci)

    start_field = Coordinate.from_uci(uci[:2])
    target_field = Coordinate.from_uci(uci[2:4])
    moving_piece = board[start_field]

    if moving_piece.type is PieceType.PAWN:
        return PawnMove.from_uci(uci)
    elif moving_piece.type is PieceType.KNIGHT:
        return NormalMove.from_uci(uci)
    elif moving_piece.type is PieceType.BISHOP:
        return NormalMove.from_uci(uci)
    elif moving_piece.type is PieceType.ROOK:
        return RookMove.from_uci(uci)
    elif moving_piece.type is PieceType.QUEEN:
        return NormalMove.from_uci(uci)
    elif moving_piece.type is PieceType.KING:
        if is_castle(start_field, target_field):
            return CastleMove.from_uci(uci)
        return KingMove.from_uci(uci)


def is_castle(start: Coordinate, end: Coordinate) -> bool:
    return abs(start.x - end.x) == 2

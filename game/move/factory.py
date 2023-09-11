from functools import cache

from game.coordinate import Coordinate
from game.move import RookMove, CastleMove, KingMove, PawnMove, PawnPromotion, NormalMove
from game.piece.piece_type import PieceType


@cache
def rook_move(start: Coordinate, end: Coordinate):
    return RookMove(start, end)


@cache
def king_move(start: Coordinate, end: Coordinate):
    return KingMove(start, end)


@cache
def castle_move(start: Coordinate, end: Coordinate):
    return CastleMove(start, end)


@cache
def pawn_move(start: Coordinate, end: Coordinate):
    return PawnMove(start, end)


@cache
def pawn_promotion(start: Coordinate, end: Coordinate,
                   promote_to: PieceType):
    return PawnPromotion(start, end, promote_to)


@cache
def en_passant(start: Coordinate, end: Coordinate):
    return PawnMove(start, end)


@cache
def knight_move(start: Coordinate, end: Coordinate):
    return NormalMove(start, end)


@cache
def bishop_move(start: Coordinate, end: Coordinate):
    return NormalMove(start, end)


@cache
def queen_move(start: Coordinate, end: Coordinate):
    return NormalMove(start, end)


@cache
def from_type(piece_type: PieceType, start: Coordinate, end: Coordinate):
    if piece_type is PieceType.ROOK:
        return rook_move(start, end)
    if piece_type is PieceType.KING:
        return king_move(start, end)
    if piece_type is PieceType.PAWN:
        return pawn_move(start, end)
    if piece_type is PieceType.KNIGHT:
        return knight_move(start, end)
    if piece_type is PieceType.BISHOP:
        return bishop_move(start, end)
    if piece_type is PieceType.QUEEN:
        return queen_move(start, end)

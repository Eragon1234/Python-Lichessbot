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


PIECE_TYPE_TO_FACTORY = {
    PieceType.ROOK: rook_move,
    PieceType.KING: king_move,
    PieceType.PAWN: pawn_move,
    PieceType.KNIGHT: knight_move,
    PieceType.BISHOP: bishop_move,
    PieceType.QUEEN: queen_move,
}


@cache
def from_type(piece_type: PieceType, start: Coordinate, end: Coordinate):
    return PIECE_TYPE_TO_FACTORY[piece_type](start, end)

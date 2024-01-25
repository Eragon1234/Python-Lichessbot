from dataclasses import dataclass
from functools import cache
from typing import Callable, Optional

from game.coordinate import Coordinate
from game.move import king, rook, pawn, normal
from game.move.board import Board
from game.piece.piece_type import PieceType


@dataclass
class Move:
    func: Callable

    start_field: Coordinate
    target_field: Coordinate

    promote_to: Optional[PieceType] = None

    def move(self, board: Board):
        if self.promote_to:
            return self.func(self.start_field, self.target_field, self.promote_to, board)
        return self.func(self.start_field, self.target_field, board)

    def uci(self) -> str:
        if self.promote_to:
            return f"{self.start_field.uci()}{self.target_field.uci()}{self.promote_to.fen()}"
        return f"{self.start_field.uci()}{self.target_field.uci()}"


@cache
def rook_move(start: Coordinate, end: Coordinate):
    return Move(rook.rook_move, start, end)


@cache
def king_move(start: Coordinate, end: Coordinate):
    return Move(king.king_move, start, end)


@cache
def castle_move(start: Coordinate, end: Coordinate):
    return Move(king.castle_move, start, end)


@cache
def pawn_move(start: Coordinate, end: Coordinate):
    return Move(pawn.pawn_move, start, end)


@cache
def pawn_promotion(start: Coordinate, end: Coordinate,
                   promote_to: PieceType):
    return Move(pawn.pawn_promotion, start, end, promote_to)


@cache
def en_passant(start: Coordinate, end: Coordinate):
    return Move(pawn.pawn_move, start, end)


@cache
def knight_move(start: Coordinate, end: Coordinate):
    return Move(normal.normal_move, start, end)


@cache
def bishop_move(start: Coordinate, end: Coordinate):
    return Move(normal.normal_move, start, end)


@cache
def queen_move(start: Coordinate, end: Coordinate):
    return Move(normal.normal_move, start, end)


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

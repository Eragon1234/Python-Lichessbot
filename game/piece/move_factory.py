from typing import Protocol, TypeVar

from game.coordinate import Coordinate
from game.piece.piece_type import PieceType

Move = TypeVar("Move")


class MoveFactory(Protocol):
    def rook_move(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def king_move(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def castle_move(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def pawn_move(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def en_passant(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def pawn_promotion(self, start: Coordinate, end: Coordinate,
                       promote_to: PieceType) -> Move:
        ...

    def knight_move(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def bishop_move(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def queen_move(self, start: Coordinate, end: Coordinate) -> Move:
        ...

    def from_type(self, piece_type: PieceType,
                  start: Coordinate, end: Coordinate) -> Move:
        """
        Create a move for the piece type and coordinates.
        Ignores special moves like castling and en passant.

        Args:
            piece_type: The type of piece being moved.
            start: The starting coordinate of the move.
            end: The ending coordinate of the move.

        Returns:
            Move: The Move object representing the requested move.
        """
        ...

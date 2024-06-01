from typing import Iterator

from game.coordinate import Coordinate
from game.piece.board import Board
from game.piece.move_factory import MoveFactory
from game.piece.moves.general import _moves_with_move_groups
from game.piece.moves.king import _king_moves
from game.piece.moves.pawn import _moves_for_pawn
from game.piece.piece_type import PieceType


def generate_moves(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate) -> Iterator:
    """
    Generates possible moves for a piece on the given chess board.

    Args:
        piece_type: The piece type
        board: The chess board.
        factory: Factory for creating moves.
        pos: The current position of the piece.

    Returns:
        A generator object that yields possible moves for the piece.
    """
    if PieceType.KING not in piece_type:
        yield from _moves_with_move_groups(piece_type, factory, board, pos)

    if PieceType.PAWN in piece_type:
        yield from _moves_for_pawn(piece_type, factory, board, pos)

    if PieceType.KING in piece_type:
        yield from _king_moves(piece_type, factory, board, pos)

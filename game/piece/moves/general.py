from typing import Iterator

from game.coordinate import Coordinate
from game.piece.board import Board
from game.piece.move_factory import MoveFactory
from game.piece.move_groups import MOVE_GROUPS
from game.piece.piece_type import PieceType


def _moves_with_move_groups(piece_type: PieceType, factory: MoveFactory, board: Board,
                            pos: Coordinate) -> Iterator:
    """
    Generates possible moves for a piece on the given chess board.

    Args:
        board: The chess board.
        pos: The current position of the piece.

    Returns:
        A generator object that yields possible moves for the piece.
    """
    for move_group in MOVE_GROUPS[piece_type.type]:
        for move in move_group:
            new_pos = pos + move

            if new_pos.out_of_bounds():
                break

            if board.is_type(new_pos, piece_type & PieceType.COLORS):
                break

            yield factory.from_type(piece_type.type, pos, new_pos)

            if not board.is_type(new_pos, PieceType.EMPTY):
                break

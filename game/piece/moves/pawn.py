from typing import Iterator

from game.coordinate import Coordinate
from game.piece.board import Board
from game.piece.move_factory import MoveFactory
from game.piece.move_groups import FORWARD, LEFT, RIGHT
from game.piece.moves.helpers import is_start_rank
from game.piece.piece_type import PieceType


def _moves_for_pawn(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate) -> Iterator:
    """
    Generates possible moves for a pawn on the given chess board.

    Args:
        board: The chess board.
        pos: The current position of the pawn.

    Returns:
        A generator object that yields possible moves for the pawn.
    """
    promote = is_start_rank(pos, piece_type.color.enemy())
    for target in _positions_for_pawn(piece_type, board, pos):
        if not promote:
            yield factory.pawn_move(pos, target)
            continue

        for piece_type in PROMOTE_TYPES:
            yield factory.pawn_promotion(pos, target,
                                         promote_to=piece_type)


def _positions_for_pawn(piece_type: PieceType, board: Board, pos: Coordinate) -> Iterator[Coordinate]:
    """
    Generates possible positions for a pawn on the given chess board.
    """
    forward = FORWARD
    if PieceType.BLACK in piece_type:
        forward = -forward

    possible_target = pos + forward
    if board.is_type(possible_target, PieceType.EMPTY):
        yield possible_target

        if is_start_rank(pos, piece_type.color):
            possible_target = pos + 2 * forward
            if board.is_type(possible_target, PieceType.EMPTY):
                yield possible_target

    possible_target = pos + LEFT + forward
    if not possible_target.out_of_bounds() and board.is_type(possible_target, piece_type.enemy):
        yield possible_target

    if board.en_passant == possible_target:
        yield board.en_passant

    possible_target = pos + RIGHT + forward
    if not possible_target.out_of_bounds() and board.is_type(possible_target, piece_type.enemy):
        yield possible_target

    if board.en_passant == possible_target:
        yield board.en_passant


PROMOTE_TYPES = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP,
                 PieceType.KNIGHT]

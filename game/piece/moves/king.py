from typing import Iterator

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.board import Board
from game.piece.move_factory import MoveFactory
from game.piece.moves.general import _moves_with_move_groups
from game.piece.piece_type import PieceType


def _king_moves(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate) -> Iterator:
    """
    Generates possible moves for a king on the given chess board.
    """
    for move in _moves_with_move_groups(piece_type, factory, board, pos):
        yield factory.king_move(move.start_field,
                                move.target_field)

    yield from _castling_moves(piece_type, factory, board, pos)


def _castling_moves(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate) -> Iterator:
    """
    Generates possible castling moves for a king on the given chess board.
    """
    if board.castling_rights is CastlingRights.NONE:
        return

    castling: list[tuple[Coordinate, int]] = []
    king = pos
    if PieceType.WHITE in piece_type:
        if CastlingRights.WHITE_KING in board.castling_rights:
            castling.append((Coordinate(7, 0), 1))
        if CastlingRights.WHITE_QUEEN in board.castling_rights:
            castling.append((Coordinate(0, 0), -1))
    else:
        if CastlingRights.BLACK_KING in board.castling_rights:
            castling.append((Coordinate(0, 7), -1))
        if CastlingRights.BLACK_QUEEN in board.castling_rights:
            castling.append((Coordinate(7, 7), 1))

    for rook, steps in castling:
        for x in range(king.x + steps, rook.x, steps):
            if not board.is_type(Coordinate(x, king.y), PieceType.EMPTY):
                break
        else:
            target = king.x + 2 * steps
            yield factory.castle_move(king,
                                      Coordinate(target, king.y))

from collections.abc import Iterator
from typing import Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.board import Board
from game.piece.color import Color
from game.piece.move_factory import MoveFactory
from game.piece.move_groups import FORWARD, LEFT, RIGHT, MOVE_GROUPS
from game.piece.piece_type import PieceType

PROMOTE_TYPES = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP,
                 PieceType.KNIGHT]


def moves(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate,
          en_passant: Optional[Coordinate] = None,
          castling_rights: CastlingRights = CastlingRights.NONE) -> Iterator:
    """
    Generates possible moves for a piece on the given chess board.

    Args:
        piece_type: The piece type
        board: The chess board.
        factory: Factory for creating moves.
        pos: The current position of the piece.
        en_passant: Optional en passant position.
        castling_rights: Optional castling rights.

    Returns:
        A generator object that yields possible moves for the piece.
    """
    if PieceType.KING not in piece_type:
        yield from _moves_with_move_groups(piece_type, factory, board, pos)

    if PieceType.PAWN in piece_type:
        yield from _moves_for_pawn(piece_type, factory, board, pos, en_passant)

    if PieceType.KING in piece_type:
        yield from _king_moves(piece_type, factory, board, pos, castling_rights)


def _king_moves(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate,
                castling_rights: CastlingRights) -> Iterator:
    """
    Generates possible moves for a king on the given chess board.
    """
    for move in _moves_with_move_groups(piece_type, factory, board, pos):
        yield factory.king_move(move.start_field,
                                move.target_field)

    yield from _castling_moves(piece_type, factory, board, pos, castling_rights)


def _castling_moves(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate,
                    castling_rights: CastlingRights) -> Iterator:
    """
    Generates possible castling moves for a king on the given chess board.
    """
    if castling_rights is CastlingRights.NONE:
        return

    castling: list[tuple[Coordinate, int]] = []
    king = pos
    if PieceType.WHITE in piece_type:
        if CastlingRights.WHITE_KING in castling_rights:
            castling.append((Coordinate(7, 0), 1))
        if CastlingRights.WHITE_QUEEN in castling_rights:
            castling.append((Coordinate(0, 0), -1))
    else:
        if CastlingRights.BLACK_KING in castling_rights:
            castling.append((Coordinate(0, 7), -1))
        if CastlingRights.BLACK_QUEEN in castling_rights:
            castling.append((Coordinate(7, 7), 1))

    for rook, steps in castling:
        for x in range(king.x + steps, rook.x, steps):
            if not board.is_type(Coordinate(x, king.y), PieceType.EMPTY):
                break
        else:
            target = king.x + 2 * steps
            yield factory.castle_move(king,
                                      Coordinate(target, king.y))


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


def _moves_for_pawn(piece_type: PieceType, factory: MoveFactory, board: Board, pos: Coordinate,
                    en_passant: Optional[Coordinate] = None) -> Iterator:
    """
    Generates possible moves for a pawn on the given chess board.

    Args:
        board: The chess board.
        pos: The current position of the pawn.
        en_passant: The position where a pawn could move en passant.

    Returns:
        A generator object that yields possible moves for the pawn.
    """
    promote = is_start_rank(pos, piece_type.color.enemy())
    for target in _positions_for_pawn(piece_type, board, pos, en_passant):
        if not promote:
            yield factory.pawn_move(pos, target)
            continue

        for piece_type in PROMOTE_TYPES:
            yield factory.pawn_promotion(pos, target,
                                         promote_to=piece_type)


def _positions_for_pawn(piece_type: PieceType, board: Board, pos: Coordinate,
                        en_passant: Optional[Coordinate] = None) -> Iterator[Coordinate]:
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

    if en_passant == possible_target:
        yield en_passant

    possible_target = pos + RIGHT + forward
    if not possible_target.out_of_bounds() and board.is_type(possible_target, piece_type.enemy):
        yield possible_target

    if en_passant == possible_target:
        yield en_passant


def is_start_rank(pos: Coordinate, color: Color) -> bool:
    """
    Checks if a given position is the start rank for a pawn of the color.

    Args:
        pos: The position to check.
        color: The color of the pawn.
        Defaults to the color of the piece.

    Returns:
        bool: whether the position is the start rank for a pawn.
    """
    start_rank = 1 if color is Color.WHITE else 6
    return pos.y == start_rank

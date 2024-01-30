from functools import partial

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move.board import Board
from game.move.move import move
from game.move.normal import normal_move
from game.piece.piece_type import PieceType


def king_move(start_field: Coordinate, target_field: Coordinate, board: Board):
    normal_move(start_field, target_field, board)

    update_castling_rights(target_field, board)


def update_castling_rights(target_field: Coordinate, board: Board) -> None:
    if board.is_type(target_field, PieceType.WHITE):
        remove_rights = CastlingRights.WHITE
    else:
        remove_rights = CastlingRights.BLACK

    board.castling_rights &= ~remove_rights


def castle_move(start_field: Coordinate, target_field: Coordinate, board: Board):
    king_move(start_field, target_field, board)

    get_rook_move(target_field)(board)


def get_rook_move(target_field: Coordinate):
    if target_field.x == 1:
        rook_start = Coordinate(0, target_field.y)
        rook_target = Coordinate(2, target_field.y)
    else:
        rook_start = Coordinate(7, target_field.y)
        rook_target = Coordinate(4, target_field.y)

    return partial(move, rook_start, rook_target)

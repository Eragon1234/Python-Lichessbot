from typing import Optional

from game.coordinate import Coordinate
from game.move.board import Board
from game.move.normal import normal_move
from game.piece.piece_type import PieceType


def pawn_move(start_field: Coordinate, target_field: Coordinate, board: Board):
    normal_move(start_field, target_field, board)

    en_passant_coord = en_passant_coordinate(start_field, target_field, board)
    if en_passant_coord is not None:
        board.pop(en_passant_coord)

    if is_double_move(start_field, target_field) and next_to_pawn(target_field, board):
        board.en_passant = new_en_passant(start_field, target_field, board)

    board.halfmove_clock = 0


def en_passant_coordinate(start_field: Coordinate, target_field: Coordinate, board: Board) -> Optional[Coordinate]:
    if board.en_passant is None:
        return None

    if target_field != board.en_passant:
        return None

    if board.is_type(start_field.value, PieceType.WHITE):
        return Coordinate(board.en_passant.x, board.en_passant.y + 1)
    return Coordinate(board.en_passant.x, board.en_passant.y - 1)


def next_to_pawn(target_field: Coordinate, board: Board) -> bool:
    if target_field.x != 0:
        left = Coordinate(target_field.x - 1, target_field.y)
        if board.is_type(left.value, PieceType.PAWN):
            return True
    if target_field.x != 7:
        right = Coordinate(target_field.x + 1, target_field.y)
        if board.is_type(right.value, PieceType.PAWN):
            return True
    return False


def is_double_move(start_field: Coordinate, target_field: Coordinate) -> bool:
    return abs(start_field.y - target_field.y) == 2


def new_en_passant(start_field: Coordinate, target_field: Coordinate, board: Board) -> Coordinate:
    if board.is_type(target_field.value, PieceType.WHITE):
        return Coordinate(start_field.x, start_field.y + 1)
    return Coordinate(start_field.x, start_field.y - 1)


def pawn_promotion(start_field: Coordinate, target_field: Coordinate, promote_to: PieceType,
                   board: Board):
    pawn_move(start_field, target_field, board)
    piece = board[target_field]
    piece.type = promote_to
    board[target_field] = piece

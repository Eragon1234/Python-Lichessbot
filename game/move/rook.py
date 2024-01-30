from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move.board import Board
from game.move.normal import normal_move
from game.piece.piece_type import PieceType


def rook_move(start_field: Coordinate, target_field: Coordinate, board: Board):
    update_castling_rights(start_field, board)

    normal_move(start_field, target_field, board)


def update_castling_rights(start_field: Coordinate, board: Board):
    if start_field.x == 0:
        remove_rights = CastlingRights.KING
    elif start_field.x == 7:
        remove_rights = CastlingRights.QUEEN
    else:
        return

    if board.is_type(start_field, PieceType.WHITE):
        remove_rights = remove_rights & CastlingRights.WHITE
    else:
        remove_rights = remove_rights & CastlingRights.BLACK

    board.castling_rights &= ~remove_rights

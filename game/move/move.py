from game.coordinate import Coordinate
from game.move.board import Board
from game.piece.piece_type import PieceType


def move(start_field: Coordinate, target_field: Coordinate, board: Board) -> PieceType:
    return board.do_move(start_field, target_field)

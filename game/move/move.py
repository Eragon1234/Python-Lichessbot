from game.coordinate import Coordinate
from game.move.board import Board, Piece


def move(start_field: Coordinate, target_field: Coordinate, board: Board) -> Piece:
    return board.do_move(start_field, target_field)

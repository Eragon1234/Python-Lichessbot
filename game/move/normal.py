from game.coordinate import Coordinate
from game.move.board import Board
from game.move.move import move
from game.piece.color import Color
from game.piece.piece_type import PieceType


def normal_move(start_field: Coordinate, target_field: Coordinate, board: Board):
    captured_piece = move(start_field, target_field, board)

    board.turn = board.turn.enemy()

    board.en_passant = None

    if captured_piece.type is not PieceType.EMPTY:
        board.halfmove_clock = -1

    board.halfmove_clock += 1

    if board.turn is Color.WHITE:
        board.fullmove_number += 1

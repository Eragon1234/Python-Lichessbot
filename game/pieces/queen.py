from game.pieces.abstract_piece import AbstractPiece
from game.pieces.bishop import Bishop
from game.pieces.rook import Rook


class Queen(AbstractPiece):
    value = 90
    short = 'q'
    bonus_map = [
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 0, 0],
        [0, 0, 2, 5, 5, 2, 0, 0],
        [0, 0, 2, 5, 5, 2, 0, 0],
        [0, 0, 2, 2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5]
    ]

    possible_move_groups = Bishop.possible_move_groups + Rook.possible_move_groups

    def __init__(self, is_white: bool):
        super().__init__(is_white)

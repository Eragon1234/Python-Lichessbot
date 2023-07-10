from game.pieces.abstract_piece import AbstractPiece


class Knight(AbstractPiece):
    value = 30
    lower_short = 'n'
    bonus_map = [
        [-5, -5, -5, -5, -5, -5, -5, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 10, 0, 0, 10, 0, -5],
        [-5, 0, 0, 3, 3, 0, 0, -5],
        [-5, 0, 0, 3, 3, 0, 0, -5],
        [-5, 0, 10, 0, 0, 10, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, -5, -5, -5, -5, -5, -5, -5]
    ]

    possible_move_groups = [
        [(i, j)] for i in [-2, -1, 1, 2] for j in [-2, -1, 1, 2] if abs(i) != abs(j)
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

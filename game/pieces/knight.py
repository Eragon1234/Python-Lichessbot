from game.pieces.abstract_piece import AbstractPiece


class Knight(AbstractPiece):
    value = 30
    short = 'n'
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
        [(-2, -1)],
        [(-2, 1)],
        [(-1, -2)],
        [(-1, 2)],
        [(1, -2)],
        [(1, 2)],
        [(2, -1)],
        [(2, 1)]
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

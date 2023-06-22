from game.pieces.abstract_piece import AbstractPiece


class King(AbstractPiece):
    value = 900
    short = 'k'
    bonus_map = [
        [0, 10, 10, 0, 0, 0, 10, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 10, 10, 0, 0, 0, 10, 0]
    ]

    possible_move_groups = [
        [(i, j)] for i in (-1, 0, 1) for j in (-1, 0, 1) if i != 0 or j != 0
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

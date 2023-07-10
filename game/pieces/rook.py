from game.pieces.abstract_piece import AbstractPiece


class Rook(AbstractPiece):
    value = 50
    lower_short = 'r'
    bonus_map = [
        [0, 0, 5, 7, 7, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 7, 7, 0, 3, 0]
    ]

    possible_move_groups = [
        [(i, 0) for i in range(1, 8)],
        [(-i, 0) for i in range(1, 8)],
        [(0, i) for i in range(1, 8)],
        [(0, -i) for i in range(1, 8)],
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

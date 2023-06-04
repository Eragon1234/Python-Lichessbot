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
        [(-1, -1)], [(-1, 0)], [(-1, 1)],  # up
        [(0, -1)], [(0, 1)],  # left and right
        [(1, -1)], [(1, 0)], [(1, 1)]  # down
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

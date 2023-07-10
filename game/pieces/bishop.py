from game.pieces.abstract_piece import AbstractPiece


class Bishop(AbstractPiece):
    value = 30
    lower_short = 'b'
    bonus_map = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 3, 3, 0, 5, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 3, 5, 0, 0, 5, 3, 0],
        [0, 3, 5, 0, 0, 5, 3, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 5, 0, 3, 3, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    possible_move_groups = [
        [(i, i) for i in range(1, 8)],
        [(i, -i) for i in range(1, 8)],
        [(-i, i) for i in range(1, 8)],
        [(-i, -i) for i in range(1, 8)]
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

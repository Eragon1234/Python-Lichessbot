import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.AbstractPiece import AbstractPiece


class Bishop(AbstractPiece):
    value = 30
    short = 'b'
    bonus_map = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 3, 3, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 5, 0, 0],
        [0, 0, 5, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 3, 3, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, is_white):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position, board):
        self.position = current_position

        positions = []

        x = current_position[0]
        y = current_position[1]
        while 6 >= x >= -1 and 6 >= y >= -1:
            x += 1
            y += 1
            position = (x, y)
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break
        x = current_position[0]
        y = current_position[1]
        while 1 <= x <= 7 and 1 <= y <= 7:
            x -= 1
            y -= 1
            position = (x, y)
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break
        x = current_position[0]
        y = current_position[1]
        while 6 >= x >= -1 and 7 >= y >= 1:
            x += 1
            y -= 1
            position = (x, y)
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break
        x = current_position[0]
        y = current_position[1]
        while 7 >= x >= 1 and 6 >= y >= -1:
            x -= 1
            y += 1
            position = (x, y)
            position = (x, y)
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break

        positions = self.filter_positions(positions)

        self.positions = positions

        return positions
import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.AbstractPiece import AbstractPiece


class King(AbstractPiece):
    value = 900
    short = 'k'

    def __init__(self, is_white):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position, board):
        positions = []
        for x in range(current_position[0] - 1, current_position[0] + 2):
            for y in range(current_position[1] - 1, current_position[1] + 2):
                position = ( x, y )
                if 0 <= x <= 7 and 0 <= y <= 7:
                    targetFieldIsWhite = board[y][x]
                    if targetFieldIsWhite == self.isWhite:
                        continue
                    elif position != current_position:
                        positions.append(position)
        positions = list(filter(lambda position: 0 <= position[0] <= 7 and 0 <= position[1] <= 7, positions))
        self.position = position
        self.positions = positions
        return positions

    def get_value(self):
        return self.value + ((len(self.positions) / 100) * self.direction_multiplier)

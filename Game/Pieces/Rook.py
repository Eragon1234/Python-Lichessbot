import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.AbstractPiece import AbstractPiece


class Rook(AbstractPiece):
    value = 50
    short = 'r'

    def __init__(self, is_white):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position, board):
        positions = []
        for x in range(current_position[0] + 1, 8):
            position = (x, current_position[1])
            targetFieldIsWhite = board[current_position[1]][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        for x in range(current_position[0] - 1, -1, -1):
            position = (x, current_position[1])
            targetFieldIsWhite = board[current_position[1]][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        for y in range(current_position[1] + 1, 8):
            position = (current_position[0], y)
            targetFieldIsWhite = board[y][current_position[0]]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        for y in range(current_position[1] - 1, -1, -1):
            position = (current_position[0], y)
            targetFieldIsWhite = board[y][current_position[0]]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        self.position = position
        self.positions = positions
        return positions

    def get_value(self):
        return self.value + ((len(self.positions) / 100) * self.direction_multiplier)
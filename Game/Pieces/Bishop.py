import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.AbstractPiece import AbstractPiece


class Bishop(AbstractPiece):
    value = 30
    short = 'b'

    def __init__(self, is_white):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position, board):
        positions = []

        x = current_position[0]
        y = current_position[1]
        while 6 >= x >= -1 and 6 >= y >= -1:
            x += 1
            y += 1
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        x = current_position[0]
        y = current_position[1]
        while 1 <= x <= 7 and 1 <= y <= 7:
            x -= 1
            y -= 1
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        x = current_position[0]
        y = current_position[1]
        while 6 >= x >= -1 and 7 >= y >= 1:
            x += 1
            y -= 1
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        x = current_position[0]
        y = current_position[1]
        while 7 >= x >= 1 and 6 >= y >= -1:
            x -= 1
            y += 1
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        positions = list(
            filter(lambda position: 0 <= position[0] <= 7 and 0 <= position[1] <= 7,
                   positions))
        self.position = position
        self.positions = positions
        return positions

    def get_value(self):
        return self.value + ((len(self.positions) / 100) * self.direction_multiplier)

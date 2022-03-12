import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.AbstractPiece import AbstractPiece

class Pawn(AbstractPiece):
    value = 10
    short = 'p'

    def __init__(self, is_white):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position, board):
        positions = []
        if self.isWhite:
            directionMultiplier = 1
        else:
            directionMultiplier = -1

        x = current_position[0]
        y = current_position[1] + (1 * directionMultiplier)
        position = (x, y)
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            targetFieldIsEmpty = board[y][x]
            if targetFieldIsEmpty == 'EmptyField':
                positions.append(position)
                y = current_position[1] + (2 * directionMultiplier)
                enPassantPosition = (x, y)
                if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                    fieldIsEmpty = board[y][x] == 'EmptyField'
                    if fieldIsEmpty:
                        if self.isWhite and current_position[1] == 1:
                            positions.append((enPassantPosition, ("enPassant", position)))
                        elif (not self.isWhite) and current_position[1] == 6:
                            positions.append((enPassantPosition, ("enPassant", position)))


        y = current_position[1] + (1 * directionMultiplier)

        x = current_position[0] + 1
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x] 
            if (targetFieldIsWhite != self.isWhite) and (targetFieldIsWhite != "EmptyField"):
                positions.append(position)

        x = current_position[0] - 1
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if (targetFieldIsWhite != self.isWhite) and (targetFieldIsWhite != "EmptyField"):
                positions.append(position)

        self.position = position
        self.positions = positions
        return positions

    def get_value(self):
        return self.value + ((len(self.positions) / 100) * self.direction_multiplier)
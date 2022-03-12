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
        if 0 <= x <= 7 and 0 <= y <= 7:
            target_field_is_empty = board[y][x]
            if target_field_is_empty == 'EmptyField':
                positions.append(position)
                y = current_position[1] + (2 * directionMultiplier)
                en_passant_position = (x, y)
                if 0 <= x <= 7 and 0 <= y <= 7:
                    field_is_empty = board[y][x] == 'EmptyField'
                    if field_is_empty:
                        if self.isWhite and current_position[1] == 1:
                            positions.append((en_passant_position, ("enPassant", position)))
                        elif (not self.isWhite) and current_position[1] == 6:
                            positions.append((en_passant_position, ("enPassant", position)))

        y = current_position[1] + (1 * directionMultiplier)

        x = current_position[0] + 1
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            position = (x, y)
            target_field_is_white = board[y][x]
            if (target_field_is_white != self.isWhite) and (target_field_is_white != "EmptyField"):
                positions.append(position)

        x = current_position[0] - 1
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            position = (x, y)
            target_field_is_white = board[y][x]
            if (target_field_is_white != self.isWhite) and (target_field_is_white != "EmptyField"):
                positions.append(position)

        self.position = position
        self.positions = positions
        return positions

    def get_value(self):
        return self.value + ((len(self.positions) / 100) * self.direction_multiplier)

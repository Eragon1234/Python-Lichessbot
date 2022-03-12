import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.AbstractPiece import AbstractPiece


class Knight(AbstractPiece):
    value = 30
    short = 'n'

    def __init__(self, is_white):
        super().__init__(is_white)
    
    def generate_possible_positions(self, current_position, board):
        positions = []
        x = current_position[0] - 1
        y = current_position[1] - 2
        self.check_if_position_is_legal(board, positions, x, y)
        
        x = current_position[0] + 1
        y = current_position[1] - 2
        self.check_if_position_is_legal(board, positions, x, y)
        
        x = current_position[0] + 2
        y = current_position[1] + 1
        self.check_if_position_is_legal(board, positions, x, y)

        x = current_position[0] + 1
        y = current_position[1] + 2
        self.check_if_position_is_legal(board, positions, x, y)

        x = current_position[0] - 1
        y = current_position[1] + 2
        self.check_if_position_is_legal(board, positions, x, y)
        
        x = current_position[0] - 2
        y = current_position[1] + 1
        self.check_if_position_is_legal(board, positions, x, y)

        x = current_position[0] - 2
        y = current_position[1] - 1
        self.check_if_position_is_legal(board, positions, x, y)
        
        x = current_position[0] + 2
        y = current_position[1] - 1
        self.check_if_position_is_legal(board, positions, x, y)

        positions = list(filter(lambda position: 0 <= position[0] <= 7 and 0 <= position[1] <= 7, positions))
        self.position = current_position
        self.positions = positions
        return positions

    def check_if_position_is_legal(self, board, positions, x, y):
        if 0 <= x <= 7 and 0 <= y <= 7:
            position = (x, y)
            target_field_is_white = board[y][x]
            if not (target_field_is_white == self.isWhite):
                positions.append(position)

    def get_value(self, position=(0, 0)):
        possible_moves_bonus = (len(self.positions) / 100) * self.direction_multiplier
        rim_position_deduction = abs((position[0] * position[1] - 15) / 15) * self.direction_multiplier

        return self.value + possible_moves_bonus + rim_position_deduction

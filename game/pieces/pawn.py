from game.pieces.abstract_piece import AbstractPiece
from game.types import Position, BoardArray, Positions


class Pawn(AbstractPiece):
    value = 10
    short = 'p'
    bonus_map = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 0.5, 0, 0, 0.5, 0, 1],
        [-1, 0, 0, 5, 5, 0, 0, -1],
        [-1, 0, 0, 5, 5, 0, 0, -1],
        [1, 0, 0.5, 0, 0, 0.5, 0, 1],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)
        self.target_field_conditions = [
            'EmptyField'
        ]

    def generate_possible_positions(self, current_position: Position, board: BoardArray) -> Positions:
        positions = []

        x = current_position[0]
        y = current_position[1]

        legal_move = self.check_if_position_is_legal(board, positions, x, y + 1 * self.direction_multiplier)
        if legal_move:
            if self.is_white and y == 1:
                self.check_if_position_is_legal(board, positions, x, y + 2 * self.direction_multiplier)
            elif not self.is_white and y == 6:
                self.check_if_position_is_legal(board, positions, x, y + 2 * self.direction_multiplier)

        self.check_if_position_is_legal(board, positions, x + 1, y + 1 * self.direction_multiplier,
                                        {not self.is_white, "enemy"})

        self.check_if_position_is_legal(board, positions, x - 1, y + 1 * self.direction_multiplier,
                                        {not self.is_white, "enemy"})

        return positions

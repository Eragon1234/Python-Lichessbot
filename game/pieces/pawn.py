from game.pieces.abstract_piece import AbstractPiece
from game.pieces.types import Position, BoardArray, Positions


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
        self.position = current_position

        positions = []

        x = current_position[0]
        y = current_position[1] + (1 * self.direction_multiplier)
        position = (x, y)
        target_field = self.check_if_position_is_legal(board, positions, *position)
        if target_field is not None:
            y = current_position[1] + (2 * self.direction_multiplier)
            en_passant_position = (x, y)
            if 0 <= x <= 7 and 0 <= y <= 7:
                field_is_empty = board[y][x] == 'EmptyField'
                if field_is_empty:
                    if self.is_white and current_position[1] == 1:
                        positions.append((en_passant_position, ("enPassant", position)))
                    elif (not self.is_white) and current_position[1] == 6:
                        positions.append((en_passant_position, ("enPassant", position)))

        y = current_position[1] + (1 * self.direction_multiplier)

        x = current_position[0] + 1
        position = (x, y)
        self.check_if_position_is_legal(board, positions, *position, [not self.is_white, "enemy"])

        x = current_position[0] - 1
        position = (x, y)
        self.check_if_position_is_legal(board, positions, *position, [not self.is_white, "enemy"])

        self.positions = positions
        return positions

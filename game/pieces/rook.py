from game.pieces.abstract_piece import AbstractPiece
from game.pieces.types import Position, Board, Positions


class Rook(AbstractPiece):
    value = 50
    short = 'r'
    bonus_map = [
        [0, 0, 5, 7, 7, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 7, 7, 0, 3, 0]
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position: Position, board: Board) -> Positions:
        self.position = current_position

        positions = []
        for x in range(current_position[0] + 1, 8):
            position = (x, current_position[1])
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break
        for x in range(current_position[0] - 1, -1, -1):
            position = (x, current_position[1])
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break
        for y in range(current_position[1] + 1, 8):
            position = (current_position[0], y)
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break
        for y in range(current_position[1] - 1, -1, -1):
            position = (current_position[0], y)
            target_field = self.check_if_position_is_legal(board, positions, *position)
            if (not self.is_white) == target_field:
                break
            elif target_field is None:
                break
        positions = self.filter_positions(positions)

        self.positions = positions
        return positions

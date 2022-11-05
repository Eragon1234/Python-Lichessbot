from game.pieces.abstract_piece import AbstractPiece
from game.pieces.types import Position, Board, Positions


class King(AbstractPiece):
    value = 900
    short = 'k'
    bonus_map = [
        [0, 10, 10, 0, 0, 0, 10, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 10, 10, 0, 0, 0, 10, 0]
    ]

    def __init__(self, is_white: bool):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position: Position, board: Board) -> Positions:
        self.position = current_position

        positions = []
        for x in range(current_position[0] - 1, current_position[0] + 2):
            for y in range(current_position[1] - 1, current_position[1] + 2):
                position = (x, y)
                self.check_if_position_is_legal(board, positions, *position)

        positions = self.filter_positions(positions)

        self.positions = positions

        return positions

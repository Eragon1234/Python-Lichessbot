from typing import Generator

from game.pieces.abstract_piece import AbstractPiece
from game.types import Position, BoardArray


class Pawn(AbstractPiece):
    value = 10
    lower_short = 'p'
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
        self.legal_target_colors = {
            'EmptyField'
        }

    def generate_possible_positions(self, board: BoardArray,
                                    current_position: Position) -> Generator[Position, None, None]:
        x, y = current_position

        possible_target = (x, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target):
            yield possible_target

            if self.is_start_rank(current_position):
                possible_target = (x, y + 2 * self.direction_multiplier)
                if self.is_legal_target(board, possible_target):
                    yield possible_target

        possible_target = (x + 1, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {not self.is_white, "enemy"}):
            yield possible_target

        possible_target = (x - 1, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {not self.is_white, "enemy"}):
            yield possible_target

    def is_start_rank(self, position: Position) -> bool:
        return position[1] == (1 if self.is_white else 6)

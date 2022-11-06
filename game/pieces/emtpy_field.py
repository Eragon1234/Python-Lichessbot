from game.pieces.abstract_piece import AbstractPiece
from game.pieces.types import Position, Board


class EmptyField(AbstractPiece):
    is_white = "EmptyField"
    short = 'e'
    lower_short = 'e'
    value = 0

    def __init__(self):
        super().__init__(self.is_white)

    def generate_possible_positions(self, current_position: Position, board: Board) -> list:
        return []

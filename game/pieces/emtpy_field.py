from game.pieces.abstract_piece import AbstractPiece
from game.types import Position, BoardArray


class EmptyField(AbstractPiece):
    self = None
    is_white = "EmptyField"
    short = 'e'
    lower_short = 'e'
    value = 0

    def __init__(self):
        super().__init__(self.is_white)

    def generate_possible_positions(self, current_position: Position, board: BoardArray) -> list:
        return []

    @classmethod
    def get_self(cls):
        if cls.self is None:
            cls.self = cls()
        return cls.self

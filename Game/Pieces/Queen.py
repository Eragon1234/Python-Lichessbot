import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.Bishop import Bishop
from Game.Pieces.Rook import Rook
from Game.Pieces.AbstractPiece import AbstractPiece


class Queen(AbstractPiece):
    value = 90
    short = 'q'

    def __init__(self, is_white):
        super().__init__(is_white)

    def generate_possible_positions(self, current_position, board):
        self.position = current_position

        bishop = Bishop(self.is_white)
        rook = Rook(self.is_white)
        rook_positions = rook.generate_possible_positions(current_position, board)
        bishop_positions = bishop.generate_possible_positions(current_position, board)
        positions = rook_positions + bishop_positions

        self.positions = positions
        return positions

    def get_value(self):
        return self.value + ((len(self.positions) / 100) * self.direction_multiplier)

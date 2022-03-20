from game.pieces.bishop import Bishop
from game.pieces.rook import Rook
from game.pieces.abstract_piece import AbstractPiece


class Queen(AbstractPiece):
    value = 90
    short = 'q'
    bonus_map = [
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 0, 0],
        [0, 0, 2, 5, 5, 2, 0, 0],
        [0, 0, 2, 5, 5, 2, 0, 0],
        [0, 0, 2, 2, 2, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-5, 0, 0, 0, 0, 0, 0, -5]
    ]

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

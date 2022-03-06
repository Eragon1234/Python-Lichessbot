import os, sys

sys.path.append(os.getcwd())

from Game.Pieces.Bishop import Bishop
from Game.Pieces.Rook import Rook


class Queen:
    value = 90
    short = 'q'

    positions = []

    def __init__(self, isWhite):
        self.isWhite = isWhite
        if self.isWhite:
            self.short = self.short.upper()
        else:
            self.value = self.value * -1

    def generate_possible_positions(self, currentPosition, board):
        bishop = Bishop(self.isWhite)
        rook = Rook(self.isWhite)
        rookPositions = rook.generate_possible_positions(currentPosition, board)
        bishopPositions = bishop.generate_possible_positions(currentPosition, board)
        positions = rookPositions + bishopPositions
        self.positions = positions
        return positions

    def get_value(self, position=False):
        if self.isWhite:
            directionMultiplier = 1
        else:
            directionMultiplier = -1
        return self.value + ((len(self.positions) / 100) * directionMultiplier)

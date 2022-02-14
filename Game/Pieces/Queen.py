from .Bishop import Bishop
from .Rook import Rook

class Queen:
    value = 9

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def generatePossiblePositions(self, currentPosition, board):
        bishop = Bishop(self.isWhite)
        rook = Rook(self.isWhite)
        rookPositions = rook.generatePossiblePositions(currentPosition, board)
        bishopPositions = bishop.generatePossiblePositions(currentPosition, board)
        positions = rookPositions + bishopPositions
        return positions
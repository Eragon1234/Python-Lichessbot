from .Bishop import Bishop
from .Rook import Rook

class Queen:
    value = 9
    short = 'q'

    def __init__(self, isWhite):
        self.isWhite = isWhite
        if self.isWhite:
            self.short = self.short.upper()
        else:
            self.value = self.value * -1

    def generatePossiblePositions(self, currentPosition, board):
        bishop = Bishop(self.isWhite)
        rook = Rook(self.isWhite)
        rookPositions = rook.generatePossiblePositions(currentPosition, board)
        bishopPositions = bishop.generatePossiblePositions(currentPosition, board)
        positions = rookPositions + bishopPositions
        return positions
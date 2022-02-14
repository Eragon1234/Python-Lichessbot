class EmptyField:
    isWhite = "EmptyField"
    def __init__(self):
        pass

    def generatePossiblePositions(self, currentPosition, board):
        return []
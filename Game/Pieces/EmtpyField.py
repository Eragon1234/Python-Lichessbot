class EmptyField:
    isWhite = "EmptyField"
    short = 'e'

    def __init__(self):
        pass

    def generatePossiblePositions(self, currentPosition, board):
        return []
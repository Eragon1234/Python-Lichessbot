class EmptyField:
    isWhite = "EmptyField"
    short = 'e'
    value = 0

    def __init__(self):
        pass

    def generatePossiblePositions(self, currentPosition, board):
        return []

    def getValue(self, position=False):
        return self.value
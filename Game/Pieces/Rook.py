class Rook:
    value = 5

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def generatePossiblePositions(self, currentPosition):
        positions = []
        for x in range(0, 8):
            position = (x, currentPosition[1])
            if position != currentPosition:
                positions.append(position)
        for y in range(0, 8):
            position = (currentPosition[0], y)
            if position != currentPosition:
                positions.append(position)
        return positions
class King:
    value = float('inf')

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def generatePossiblePositions(self, currentPosition):
        positions = []
        for x in range(currentPosition[0] - 1, currentPosition[0] + 2):
            for y in range(currentPosition[1] - 1, currentPosition[1] + 2):
                position = ( x, y )
                if (position[0] >= 0 and position[1] >= 0 and position[0] <= 7 and position[1] <= 7 and position != currentPosition):
                    positions.append(position)
        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
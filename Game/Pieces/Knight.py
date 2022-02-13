class Knight:
    value = 3

    def __init__(self, isWhite):
        self.isWhite = isWhite
    
    def generatePossiblePositions(self, currentPosition):
        positions = []
        position = (currentPosition[0] - 1, currentPosition[1] - 2)
        positions.append(position)
        position = (currentPosition[0] + 1, currentPosition[1] - 2)
        positions.append(position)
        position = (currentPosition[0] + 2, currentPosition[1] - 1)
        positions.append(position)
        position = (currentPosition[0] + 2, currentPosition[1] + 1)
        positions.append(position)
        position = (currentPosition[0] + 1, currentPosition[1] + 2)
        positions.append(position)
        position = (currentPosition[0] - 1, currentPosition[1] + 2)
        positions.append(position)
        position = (currentPosition[0] - 2, currentPosition[1] + 1)
        positions.append(position)
        position = (currentPosition[0] - 2, currentPosition[1] - 1)
        positions.append(position)
        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
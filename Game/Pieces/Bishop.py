class Bishop:
    value = 3

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def generatePossiblePositions(self, currentPosition):
        positions = []

        diagonal1 = (currentPosition[0], currentPosition[1])
        while (diagonal1[0] != 0 and diagonal1[1] != 0):
            diagonal1 = (diagonal1[0] - 1, diagonal1[1] - 1)

        diagonal2 = (currentPosition[0], currentPosition[1])
        while (diagonal2[0] != 0 and diagonal2[1] != 0):
            diagonal2 = (diagonal2[0] + 1, diagonal2[1] - 1)
        
        position = (diagonal1[0], diagonal1[1])
        while (position[0] != 8 and position[1] != 8 and position[0] != -1 and position[1] != -1):
            if position != currentPosition:
                positions.append(position)
            position = (position[0] + 1, position[1] + 1)

        position = (diagonal2[0], diagonal2[1])
        while (position[0] != 8 and position[1] != 8 and position[0] != -1 and position[1] != -1):
            if position != currentPosition:
                positions.append(position)
            
            position = (position[0] - 1, position[1] + 1)
        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
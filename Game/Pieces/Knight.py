class Knight:
    value = 3
    short = 'n'

    def __init__(self, isWhite):
        self.isWhite = isWhite
        if self.isWhite:
            self.short = self.short.upper()
        else:
            self.value = self.value * -1
    
    def generatePossiblePositions(self, currentPosition, board):
        positions = []
        x = currentPosition[0] - 1
        y = currentPosition[1] - 2
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)
        
        x = currentPosition[0] + 1
        y = currentPosition[1] - 2
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)
        
        x = currentPosition[0] + 2
        y = currentPosition[1] + 1
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)

        x = currentPosition[0] + 1
        y = currentPosition[1] + 2
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)

        x = currentPosition[0] - 1
        y = currentPosition[1] + 2
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)
        
        x = currentPosition[0] - 2
        y = currentPosition[1] + 1
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)

        x = currentPosition[0] - 2 
        y = currentPosition[1] - 1
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)
        
        x = currentPosition[0] + 2
        y = currentPosition[1] - 1
        if x >= 0 and y >= 0 and x <= 7 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if not (targetFieldIsWhite == self.isWhite):
                positions.append(position)

        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
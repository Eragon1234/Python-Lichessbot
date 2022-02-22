class King:
    value = 999
    short = 'k'

    def __init__(self, isWhite):
        self.isWhite = isWhite
        if self.isWhite:
            self.short = self.short.upper()
        else:
            self.value = self.value * -1

    def generatePossiblePositions(self, currentPosition, board):
        positions = []
        for x in range(currentPosition[0] - 1, currentPosition[0] + 2):
            for y in range(currentPosition[1] - 1, currentPosition[1] + 2):
                position = ( x, y )
                if x >= 0 and y >= 0 and x <= 7 and y <= 7:
                    targetFieldIsWhite = board[y][x]
                    if targetFieldIsWhite == self.isWhite:
                        continue
                    elif position != currentPosition:
                        positions.append(position)
        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
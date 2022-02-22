class Pawn:
    value = 1
    short = 'p'

    def __init__(self, isWhite):
        self.isWhite = isWhite
        if self.isWhite:
            self.short = self.short.upper()
        else:
            self.value = self.value * -1

    def generatePossiblePositions(self, currentPosition, board):
        positions = []
        if self.isWhite:
            directionMultiplier = 1
        else:
            directionMultiplier = -1

        x = currentPosition[0]
        y = currentPosition[1] + (1 * directionMultiplier)
        position = (x, y)
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            targetFieldIsEmpty = board[y][x]
            if targetFieldIsEmpty == 'EmptyField':
                positions.append(position)
                y = currentPosition[1] + (2 * directionMultiplier)
                position = (x, y)
                if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                    fieldIsEmpty = board[y][x] == 'EmptyField'
                    if fieldIsEmpty:
                        if self.isWhite and position[1] == 1:
                            positions.append(position)
                        elif (not self.isWhite) and position[1] == 6:
                                positions.append(position)


        y = currentPosition[1] + (1 * directionMultiplier)

        x = currentPosition[0] + 1
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x] 
            if (targetFieldIsWhite != self.isWhite) and (targetFieldIsWhite != "EmptyField"):
                positions.append(position)

        x = currentPosition[0] - 1
        if x >= 0 and x <= 7 and y >= 0 and y <= 7:
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if (targetFieldIsWhite != self.isWhite) and (targetFieldIsWhite != "EmptyField"):
                positions.append(position)

        positions = list(filter(lambda position: (position[0] >= 0) and (position[0] <= 7) and (position[1] >= 0) and (position[1] <= 7), positions))
        return positions
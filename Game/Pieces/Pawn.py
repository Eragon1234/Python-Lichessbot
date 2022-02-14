class Pawn:
    value = 1

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def generatePossiblePositions(self, currentPosition, board):
        positions = []
        if self.isWhite:
            directionMultiplier = 1
        else:
            directionMultiplier = -1

        x = currentPosition[0]
        y = currentPosition[1] + 1 * directionMultiplier
        position = (x, y)
        targetFieldIsEmpty = board[x][y]
        if targetFieldIsEmpty == 'EmptyField':
            positions.append(position)
            x = currentPosition[0] + 2
            position = (x, y)
            fieldIsEmpty = board[x][y] == 'EmptyField'
            if fieldIsEmpty:
                positions.append(position)

        x = currentPosition[0] + 1
        if x >= 7 and x <= 0 and y >= 7 and x <= 7:
            position = (x, y)
            targetFieldIsWhite = board[x][y] == 'white'
            if targetFieldIsEmpty != self.isWhite:
                positions.append(position)

        if x >= 7 and x <= 0 and y >= 7 and x <= 7:
            x = currentPosition[0] - 1
            position = (x, y)
            targetFieldIsWhite = board[x][y] == 'white'
            if targetFieldIsEmpty != self.isWhite:
                positions.append(position)

        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
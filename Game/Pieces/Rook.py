class Rook:
    value = 5

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def generatePossiblePositions(self, currentPosition, board):
        positions = []
        for x in range(currentPosition[0] + 1, 8):
            position = (x, currentPosition[1])
            targetFieldIsWhite = board[currentPosition[1]][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        for x in range(currentPosition[0] - 1, -1):
            position = (x, currentPosition[1])
            targetFieldIsWhite = board[x][currentPosition[1]][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        for y in range(currentPosition[1] + 1, 8):
            position = (currentPosition[0], y)
            targetFieldIsWhite = board[y][currentPosition[0]]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        for y in range(currentPosition[1] - 1, -1):
            position = (currentPosition[0], y)
            targetFieldIsWhite = board[y][currentPosition[0]]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
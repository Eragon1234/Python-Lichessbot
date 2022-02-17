class Bishop:
    value = 3
    short = 'b'

    def __init__(self, isWhite):
        self.isWhite = isWhite
        if self.isWhite:
            self.short = self.short.upper()

    def generatePossiblePositions(self, currentPosition, board):
        positions = []

        x = currentPosition[0]
        y = currentPosition[1]
        while x <= 6 and x >= -1 and y <= 6 and y >= -1:
            x += 1
            y += 1
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        while x <= 7 and x >= 1 and y <= 7 and y >= 1:
            x -= 1
            y -= 1
            position = (x, y)
            targetFieldIsWhite = board[y][x] 
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        while x <= 6 and x >= -1 and y <= 7 and y >= 1:
            x += 1
            y -= 1
            position = (x, y)
            targetFieldIsWhite = board[y][x]
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        while x <= 7 and x >= 1 and y <= 6 and y >= -1:
            x -= 1
            y += 1
            position = (x, y)
            targetFieldIsWhite = board[y][x] 
            if targetFieldIsWhite == self.isWhite:
                break
            elif targetFieldIsWhite != 'EmptyField':
                positions.append(position)
                break
            else:
                positions.append(position)
        positions = list(filter(lambda position: position[0] >= 0 and position[0] <= 7 and position[1] >= 0 and position[1] <= 7, positions))
        return positions
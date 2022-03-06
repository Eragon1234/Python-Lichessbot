class Pawn:
    value = 10
    short = 'p'
    positions = []

    def __init__(self, isWhite):
        self.isWhite = isWhite
        if self.isWhite:
            self.short = self.short.upper()
        else:
            self.value = self.value * -1

    def generate_possible_positions(self, currentPosition, board):
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
                enPassantPosition = (x, y)
                if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                    fieldIsEmpty = board[y][x] == 'EmptyField'
                    if fieldIsEmpty:
                        if self.isWhite and currentPosition[1] == 1:
                            positions.append((enPassantPosition, ("enPassant", position)))
                        elif (not self.isWhite) and currentPosition[1] == 6:
                            positions.append((enPassantPosition, ("enPassant", position)))


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

        self.positions = positions
        return positions

    def get_value(self, position=False):
        if self.isWhite:
            directionMultiplier = 1
        else:
            directionMultiplier = -1
        return self.value + ((len(self.positions) / 100) * directionMultiplier)
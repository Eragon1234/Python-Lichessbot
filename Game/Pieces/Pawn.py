class Pawn:
    value = 1

    def __init__(self, isWhite):
        self.isWhite = isWhite

    def generatePossiblePositions(self, currentPosition):
        positions = []
        if self.isWhite:
            position = ( currentPosition[0], currentPosition[1] - 1 )
            positions.append(position)

            position = ( currentPosition[0] - 1, currentPosition[1] - 1, ( 'isEnemyPiece', 'isEnPassantField' ) )
            positions.append(position)

            position = ( currentPosition[0] + 1, currentPosition[1] - 1, ( 'isEnemyPiece', 'isEnPassantField' ) )
            positions.append(position)

            if currentPosition[1] == 6:
                position = ( currentPosition[0],  currentPosition[1] - 2 )
                positions.append(position)
        else:
            position = ( currentPosition[0], currentPosition[1] + 1 )
            positions.append(position)

            position = ( currentPosition[0] - 1, currentPosition[1] + 1, ( 'isEnemyPiece', 'isEnPassantField') )
            positions.append(position)

            position = ( currentPosition[0] + 1, currentPosition[1] + 1, ( 'isEnemyPiece', 'isEnPassantField' ) )
            positions.append(position)

            if currentPosition[1] == 1:
                position = ( currentPosition[0], currentPosition[1] + 2 )
                positions.append(position)
        return positions
from .Pieces.EmtpyField import EmptyField
from .Pieces.Pawn import Pawn
from .Pieces.Bishop import Bishop
from .Pieces.Knight import Knight
from .Pieces.Rook import Rook
from .Pieces.Queen import Queen
from .Pieces.King import King

class Board:
    moves = []

    def __init__(self, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.loadBoardWithFen(fen)

        self.columns = {
            '0': 'a',
            '1': 'b',
            '2': 'c',
            '3': 'd',
            '4': 'e',
            '5': 'f',
            '6': 'g',
            '7': 'h'
        }

    def move(self, move):
        self.moves.append(move)
        move = self.UCIintoCoordinateMoves(move)
        movingPiece = self.board[move[0][1]][move[0][0]]
        self.board[move[0][1]][move[0][0]] = EmptyField()
        self.board[move[1][1]][move[1][0]] = movingPiece

        flattendedBoard = sum(self.board, [])
        movedPiece = self.board[move[1][1]][move[1][0]]
        attackedFields = movedPiece.generatePossiblePositions((move[1][0], move[1][1]), self.generateColorBoard())
        for attackedField in attackedFields:
            attackedPiece = self.board[attackedField[1]][attackedField[0]]
            if attackedPiece.isWhite == 'EmptyField':
                continue
            print(attackedPiece.short)
            if (attackedPiece.short == 'K' or attackedPiece.short == 'k') and (attackedPiece.isWhite != movedPiece.isWhite):
                print("check")
                continue

    def generatePossibleMoves(self, forWhite=True):
        coordinateMoves = []
        colorBoard = self.generateColorBoard()
        flattendedBoard = sum(self.board, [])
        for piece in flattendedBoard:
            index = flattendedBoard.index(piece)
            coordinates = self.generateCoordinatesWithIndex(index)
            if piece.isWhite == forWhite:
                newPositions = piece.generatePossiblePositions(coordinates, colorBoard)
                for newPosition in newPositions:
                    coordinateMoves.append((coordinates, newPosition))
        moves = self.coordinateMovesIntoUCI(coordinateMoves)
        return moves

    def generateCoordinatesWithIndex(self, index):
        x = index % 8
        y = index // 8
        return (x, y)

    def generateColorBoard(self):
        colorBoard = []
        for row in self.board:
            colorBoard.append([])
            for piece in row:
                colorBoard[-1].append(piece.isWhite)
        return colorBoard
    def coordinateMovesIntoUCI(self, coordinateMoves):
        moves = []
        for coordinateMove in coordinateMoves:
            x1 = self.columns[f"{coordinateMove[0][0]}"]
            y1 = coordinateMove[0][1] + 1
            x2 = self.columns[f"{coordinateMove[1][0]}"]
            y2 = coordinateMove[1][1] + 1
            move = f"{x1}{y1}{x2}{y2}"
            moves.append(move)
        return moves
    
    def UCIintoCoordinateMoves(self, UCIMove):
        coordinateMove = []
        keys = list(self.columns.keys())
        values = list(self.columns.values())
        x1 = values.index(UCIMove[0])
        y1 = int(UCIMove[1]) - 1
        x2 = values.index(UCIMove[2])
        y2 = int(UCIMove[3]) - 1
        coordinateMove.append((x1, y1))
        coordinateMove.append((x2, y2))
        return coordinateMove
        
    def loadBoardWithFen(self, fen):
        board = []
        row = 0

        fen = fen.split()
        
        positionFenByRow = fen[0].split("/")

        for rowFen in positionFenByRow:
            board.append([])
            for char in rowFen:
                # checking for black pieces with fen code
                if char == 'p':
                    board[row].append(Pawn(False))
                elif char == 'b':
                    board[row].append(Bishop(False))
                elif char == 'n':
                    board[row].append(Knight(False))
                elif char == 'r':
                    board[row].append(Rook(False))
                elif char == 'q':
                    board[row].append(Queen(False))
                elif char == 'k':
                    board[row].append(King(False))
                
                # checking for white pieces with fen code
                elif char == 'P':
                    board[row].append(Pawn(True))
                elif char == 'B':
                    board[row].append(Bishop(True))
                elif char == 'N':
                    board[row].append(Knight(True))
                elif char == 'R':
                    board[row].append(Rook(True))
                elif char == 'Q':
                    board[row].append(Queen(True))
                elif char == 'K':
                    board[row].append(King(True))
                
                # checking for numbers to move n pieces further
                elif char.isdigit():
                    for i in range(0, int(char)):
                        board[row].append(EmptyField())
            row += 1
        
        if fen[1] == 'w':
            self.whitesMove = True
        else:
            self.whitesMove = False

        for char in fen[2]:
            self.whiteCastle = {}
            self.blackCastle = {}

            self.whiteCastle['KingSide'] = False
            self.whiteCastle['QueenSide'] = False

            self.blackCastle['KingSide'] = False
            self.blackCastle['QueenSide'] = False

            if char == 'K':
                self.whiteCastle['KingSide'] = True
            elif char == 'Q':
                self.whiteCastle['QueenSide'] = True
            elif char == 'k':
                self.blackCastle['KingSide'] = True
            elif char == 'q':
                self.blackCastle['QueenSide'] = True
        
        self.enPassantField = fen[3]
        self.pliesFor50MoveRule = fen[4]
        self.nextMoveNumber = fen[5]

        self.board = board
        self.board.reverse()

    def generateFenForBoard(self):
        fen = ""
        flattendedBoard = sum(self.board, [])
        for piece in flattendedBoard:
            fen += piece.short
        return fen
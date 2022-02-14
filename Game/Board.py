from ast import Continue
from .Pieces.EmtpyField import EmptyField
from .Pieces.Pawn import Pawn
from .Pieces.Bishop import Bishop
from .Pieces.Knight import Knight
from .Pieces.Rook import Rook
from .Pieces.Queen import Queen
from .Pieces.King import King

class Board:

    def __init__(self, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        board = []
        row = 0
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

    def generatePossibleMoves(self, forWhite=True):
        coordinateMoves = []
        colorBoard = []
        flattendedBoard = sum(self.board, [])
        for row in self.board:
            colorBoard.append([])
            for piece in row:
                colorBoard[-1].append(piece.isWhite)
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
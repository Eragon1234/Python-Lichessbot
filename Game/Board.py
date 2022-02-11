from Pieces.EmtpyField import EmptyField
from Pieces.Pawn import Pawn
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.Queen import Queen
from Pieces.King import King

class Board:

    def __init__(self, fen, whitesMove=True):
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

    def generatePossibleMoves(self):
        pass
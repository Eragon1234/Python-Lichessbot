from Pieces.EmtpyField import EmptyField
from Pieces.Pawn import Pawn
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.Queen import Queen
from Pieces.King import King

class Board:

    def __init__(self, fen):
        self.board = self.generateBoardArrayWithFen(fen)

    def generateBoardArrayWithFen(self, fen):
        board = []
        for char in fen:
            # checking for black pieces with fen code
            if char == 'p':
                board.append(Pawn(False))
            elif char == 'b':
                board.append(Bishop(False))
            elif char == 'n':
                board.append(Knight(False))
            elif char == 'r':
                board.append(Rook(False))
            elif char == 'q':
                board.append(Queen(False))
            elif char == 'k':
                board.append(King(False))
            
            # checking for white pieces with fen code
            elif char == 'P':
                board.append(Pawn(True))
            elif char == 'B':
                board.append(Bishop(True))
            elif char == 'N':
                board.append(Knight(True))
            elif char == 'R':
                board.append(Rook(True))
            elif char == 'Q':
                board.append(Queen(True))
            elif char == 'K':
                board.append(King(True))
            
            # checking for numbers to move n pieces further
            elif char.isdigit():
                for i in range(0, int(char)):
                    board.append(EmptyField())

            elif char == ' ':
                break

        return board
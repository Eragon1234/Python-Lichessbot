import numpy as np
from copy import deepcopy
import random

from .Pieces.EmtpyField import EmptyField
from .Pieces.Pawn import Pawn
from .Pieces.Bishop import Bishop
from .Pieces.Knight import Knight
from .Pieces.Rook import Rook
from .Pieces.Queen import Queen
from .Pieces.King import King

class Board:
    """
    a class to handle the current board state, making moves, generating possible Moves etc.
    """

    # an array for moved moves
    moves = []

    # a dictionary for board copies with test moves
    testBoards = {}

    # the corresponding letter for the indexes of the columns
    columns = {
        '0': 'a',
        '1': 'b',
        '2': 'c',
        '3': 'd',
        '4': 'e',
        '5': 'f',
        '6': 'g',
        '7': 'h'
    }

    def __init__(self, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        # loads the board with the given fen
        self.loadBoardWithFen(fen)

    def move(self, move):
        """ makes a move on the board

        Args:
            move (UCIMove): the move to move
        """

        # reseting the check to false
        self.check = False
        # appending the move to the array of moves
        self.moves.append(move)
        # converting the UCIMove into a coordinate move
        move = self.UCIintoCoordinateMove(move)
        # getting the moving piece
        movingPiece = self.board[move[0][1], move[0][0]]
        # emptying the startField
        self.board[move[0][1], move[0][0]] = EmptyField()
        # setting the targetField to the movingPiece
        self.board[move[1][1], move[1][0]] = movingPiece

        # getting the moved piece
        movedPiece = self.board[move[1][1]][move[1][0]]
        # getting the new attacked fields of the attacking piece
        attackedFields = movedPiece.generatePossiblePositions((move[1][0], move[1][1]), self.generateColorBoard())
        # checking for every attacking piece if it is attacking the opponents king
        for attackedField in attackedFields:
            attackedPiece = self.board[attackedField[1], attackedField[0]]
            if attackedPiece.isWhite == 'EmptyField':
                continue
            if (attackedPiece.short == 'K' or attackedPiece.short == 'k') and (attackedPiece.isWhite != movedPiece.isWhite):
                self.check = True
                break

        # getting the startField of the moving piece
        startField = (move[0][0], move[0][1])
        queen = Queen(True)

        # generating all diagonals and rows where a piece possibly has been opened
        possibleOpenedFields = queen.generatePossiblePositions(startField, self.generateColorBoard())
        # checking if one of the possible opened fields checked the king
        for possibleOpenedField in possibleOpenedFields:
            possibleOpenedPiece = self.board[possibleOpenedField[1], possibleOpenedField[0]]
            coordinates = np.where(self.board == possibleOpenedPiece)
            coordinates = (coordinates[1][0], coordinates[0][0])

            attackedFields = possibleOpenedPiece.generatePossiblePositions(coordinates, self.generateColorBoard())
            for attackedField in attackedFields:
                attackedPiece = self.board[attackedField[1], attackedField[0]]
                if attackedPiece.isWhite == 'EmptyField':
                    continue
                if (attackedPiece.short == 'K' or attackedPiece.short == 'k') and (attackedPiece.isWhite != movedPiece.isWhite):
                    self.check = True
                    break
        print("Check:", self.check)

    def testMove(self, move):
        """ creates a copy of the board on which the move is moved

        Args:
            move (UCIMove): the move to test on a new board

        Returns:
            string: a key to get the board from the testBoards dictionary
        """

        # converting the UCIMove into a coordinate move
        move = self.UCIintoCoordinateMove(move)

        # creating a deepcopy of the board
        board = deepcopy(self)

        # getting the moving piece
        movingPiece = board.board[move[0][1], move[0][0]]
        # emptying the startField
        board.board[move[0][1], move[0][0]] = EmptyField()
        # setting the targetField to the movingPiece
        board.board[move[1][1], move[1][0]] = movingPiece
        # reseting the check to false
        board.check = False

        # getting the moved piece
        movedPiece = board.board[move[1][1], move[1][0]]
        # getting the new attacked fields of the attacking piece
        attackedFields = movedPiece.generatePossiblePositions((move[1][0], move[1][1]), board.generateColorBoard())

        # checking for every attacking piece if it is attacking the opponents king
        for attackedField in attackedFields:
            attackedPiece = board.board[attackedField[1], attackedField[0]]
            if attackedPiece.isWhite == 'EmptyField':
                continue
            if (attackedPiece.short == 'K' or attackedPiece.short == 'k') and (attackedPiece.isWhite != movedPiece.isWhite):
                board.check = True
                break

        # getting the startField of the moving piece
        startField = (move[0][0], move[0][1])
        queen = Queen(True)
        # generating all diagonals and rows where a piece possibly has been opened
        possibleOpenedFields = queen.generatePossiblePositions(startField, board.generateColorBoard())
        # checking if one of the possible opened fields checked the king
        for possibleOpenedField in possibleOpenedFields:
            possibleOpenedPiece = board.board[possibleOpenedField[1], possibleOpenedField[0]]
            coordinates = np.where(self.board == possibleOpenedPiece)
            try:
                coordinates = (coordinates[1][0], coordinates[0][0])
            except:
                continue

            attackedFields = possibleOpenedPiece.generatePossiblePositions(coordinates, board.generateColorBoard())
            for attackedField in attackedFields:
                attackedPiece = board.board[attackedField[1], attackedField[0]]
                if attackedPiece.isWhite == 'EmptyField':
                    continue
                if (attackedPiece.short == 'K' or attackedPiece.short == 'k') and (attackedPiece.isWhite != movedPiece.isWhite):
                    board.check = True
                    break

        # generate key for access over testBoards array
        boardKey = self.generateRandomString(8)
        while boardKey in self.testBoards.keys():
            boardKey = self.generateRandomString(8)
        
        # adding the board at the random key at the testBoards array
        self.testBoards[boardKey] = board
        
        return boardKey

    def popTestBoard(self, boardKey):
        """ removes and returns the board with the given key

        Args:
            boardKey (string): the key to acces the testBoard

        Returns:
            Board: the board at the given key
        """
        return self.testBoards.pop(boardKey)

    def generatePossibleMoves(self, forWhite=True):
        """ generating all possible moves in the current position

        Args:
            forWhite (bool): for which color to generate the moves for. Defaults to True.

        Returns:
            list: a list of possible moves in UCIMove format
        """
        coordinateMoves = []
        # generating the colorBoard as a parameter for the generatePossiblePositions method of the pieces
        colorBoard = self.generateColorBoard()
        for piece in list(self.board.flat):
            # getting the coordinates of the piece in the flattened array
            coordinates = np.where(self.board == piece)
            coordinates = (coordinates[1][0], coordinates[0][0])

            # if piece is the color for which to generate moves for
            if piece.isWhite == forWhite:
                # generating possible positions
                newPositions = piece.generatePossiblePositions(coordinates, colorBoard)
                # appending every position with the start and end coordinates
                for newPosition in newPositions:
                    coordinateMoves.append((coordinates, newPosition))
        # converting coordinate moves into UCIMoves
        moves = self.coordinateMovesIntoUCI(coordinateMoves)

        # testing every move if the king is in check
        for move in moves:
            boardKey = self.testMove(move)
            if self.testBoards[boardKey].check:
                moves.remove(move)
            self.popTestBoard(boardKey)
        
        return moves

    def calculateMaterialDifference(self):
        """ caculates the material difference between white and black

        Returns:
            int: the material difference
        """
        materialDifference = 0
        
        for piece in list(self.board.flat):
            materialDifference += piece.value
        return materialDifference
    def generateCoordinatesWithIndex(self, index):
        """ calculates the coordinates of a piece on the given index in 1d array with the length 64

        Args:
            index (int): the index in the 1d array

        Returns:
            tuple: the x and y coordinates of the piece
        """
        x = index % 8
        y = index // 8
        return (x, y)

    def generateColorBoard(self):
        """ converts the current board state into a board with True, False and EmptyField as values that are standing for whitePiece, blackPiece and EmptyField

        Returns:
            list: a 2d array with values True for white, False for black and EmptyField for an empty field
        """
        colorBoard = []
        for row in self.board:
            colorBoard.append([])
            for piece in row:
                colorBoard[-1].append(piece.isWhite)
        return colorBoard
    
    def coordinateMovesIntoUCI(self, coordinateMoves):
        """ converts the passed array of coordinate moves into an array of UCIMoves

        Args:
            coordinateMoves (list): a list containing tuples with the startField and the targetField as tuples with x and y

        Returns:
            list: a list of string which are moves in the UCI Notation
        """
        moves = []
        for coordinateMove in coordinateMoves:
            x1 = self.columns[f"{coordinateMove[0][0]}"] # getting the letter for the column of the startField with the x number
            y1 = coordinateMove[0][1] + 1
            x2 = self.columns[f"{coordinateMove[1][0]}"] # getting the letter for the column of the endField with the x number
            y2 = coordinateMove[1][1] + 1

            # combining these values to a string
            move = f"{x1}{y1}{x2}{y2}"
            moves.append(move)
        return moves
    
    def UCIintoCoordinateMove(self, UCIMove):
        """ converts the passed UCIMove into a coordinate move

        Args:
            UCIMove (string): the UCIMove to convert into an UCIMove

        Returns:
            tuple: the coordinate move corresponding to the passed UCIMove
        """
        coordinateMove = []
        values = list(self.columns.values())
        x1 = values.index(UCIMove[0]) # getting the key of the letter in the UCIMove to get the x start coordinate
        y1 = int(UCIMove[1]) - 1
        x2 = values.index(UCIMove[2]) # getting the key of the letter in the UCIMove to get the x end coordinate
        y2 = int(UCIMove[3]) - 1
        coordinateMove.append((x1, y1))
        coordinateMove.append((x2, y2))
        return coordinateMove
        
    def loadBoardWithFen(self, fen):
        """ loads the board with the passed fen

        Args:
            fen (string): the fen to load the board of the board object with
        """
        board = []

        fen = fen.split()
        
        positionFenByRow = fen[0].split("/")

        for rowFen in positionFenByRow:
            board.append([])
            for char in rowFen:
                # checking for black pieces with fen code
                if char == 'p':
                    board[-1].append(Pawn(False))
                elif char == 'b':
                    board[-1].append(Bishop(False))
                elif char == 'n':
                    board[-1].append(Knight(False))
                elif char == 'r':
                    board[-1].append(Rook(False))
                elif char == 'q':
                    board[-1].append(Queen(False))
                elif char == 'k':
                    board[-1].append(King(False))
                
                # checking for white pieces with fen code
                elif char == 'P':
                    board[-1].append(Pawn(True))
                elif char == 'B':
                    board[-1].append(Bishop(True))
                elif char == 'N':
                    board[-1].append(Knight(True))
                elif char == 'R':
                    board[-1].append(Rook(True))
                elif char == 'Q':
                    board[-1].append(Queen(True))
                elif char == 'K':
                    board[-1].append(King(True))
                
                # checking for numbers to move n pieces further
                elif char.isdigit():
                    for i in range(0, int(char)):
                        board[-1].append(EmptyField())
        
        # looking if it's white or blacks turn
        if fen[1] == 'w':
            self.whitesMove = True
        else:
            self.whitesMove = False

        # setting the castle rights of black and white
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
        
        self.enPassantField = fen[3] # setting the enPassantField with the corresponding value of the fen
        self.pliesFor50MoveRule = fen[4] # setting the number of plies since the last pawn move or take for the 50 move rule
        self.nextMoveNumber = fen[5] # setting the number of the next move

        # setting self.board to the board
        board.reverse()
        board = np.array(board)
        self.board = board

    def generateFenForBoard(self):
        """ generates the fen for the current board

        Returns:
            string: the fen string for the current position on the board
        """
        fen = ""
        flattendedBoard = list(self.board.flatten()) # flattening the board
        for piece in flattendedBoard:
            fen += piece.short # adding the short of the piece to the fen string
            if (flattendedBoard.index(piece) + 1) % 8 == 0:
                fen += "/"
        return fen

    def generateRandomString(self, length):
        """ generates a random string with the specified length

        Args:
            length (int): the length the random string should be

        Returns:
            string: a random string of the specified length
        """
        randomString = ''
        for i in range(0, length):
            randomInteger = random.randint(0, 255) # getting a random integer in the range 0 to 255 which is the range of the ASCII numbers
            randomString += chr(randomInteger) # converting the number into a char and appending if to the string
        return randomString
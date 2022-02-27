from sys import float_repr_style
from Game.Board import Board
import random
import numpy as np

class Engine:
    """
    Class to generate the best possible moves etc.
    """

    def __init__(self, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = Board(fen)

    def move(self, gameId, color, moves, moveFn):
        """ handles the calculations for the best possible moves

        Args:
            gameId (string): the id of the game to move in
            color (string): the color for whom to generate the best moves
            moves (string): moves since the start position
            moveFn (fn): function to make the move
        """
        forWhite = color == 'white'
        
        bestMove = self.calculateBestMove(forWhite, 3)
        print("Evaluation:", bestMove[1])
        move = bestMove[0]
        print(move)
        self.board.move(move)
        moveFn(gameId, move)
        print("moved")

    def opponentsMove(self, move):
        self.board.move(move)
        print("opponent moved")

    def calculateBestMove(self, forWhite, depth, board=False):
        if not board:
            board = self.board

        if forWhite:
            move = self.max(depth, float("-inf"), float("inf"), board, True)
        else:
            move = self.min(depth, float("-inf"), float("inf"), board, True)
        
        return move
    
    def max(self, depth, alpha, beta, board, returnMove=False):
        moves = board.generatePossibleMoves(True)

        if len(moves) == 0:
            return float("-inf")
            
        if depth == 0:
            return self.getMaterialDifferenceForMove(moves[0])

        maxWert = alpha
        maxMove = moves[0]

        for move in moves:
            boardKey = self.board.testMove(move, board)
            evaluation = self.min(depth - 1, maxWert, beta, board.testBoards[boardKey])
            evaluation = int(evaluation)
            if evaluation > maxWert:
                maxWert = evaluation
                maxMove = move
                if maxWert >= beta:
                    break
            self.board.popTestBoard(boardKey)
        if returnMove:
            return maxMove, maxWert
        return maxWert

    def min(self, depth, alpha, beta, board, returnMove=False):
        moves = board.generatePossibleMoves(False)

        if len(moves) == 0:
            return float("inf")


        if depth == 0:
            return self.getMaterialDifferenceForMove(moves[0])
        
        minWert = beta
        minMove = moves[0]

        for move in moves:
            boardKey = self.board.testMove(move, board)
            evaluation = self.max(depth - 1, alpha, minWert, board.testBoards[boardKey])
            evaluation = int(evaluation)
            if evaluation < minWert:
                minWert = evaluation
                minMove = move
                if minWert <= alpha:
                    break
            self.board.popTestBoard(boardKey)
        if returnMove:
            return minMove, minWert
        return minWert

    def getMaterialDifferenceForMove(self, move, board=False):
        if not board:
            board = self.board
        board = self.board.popTestBoard(self.board.testMove(move, board))
        evaluation = board.calculateMaterialDifference()
        return evaluation
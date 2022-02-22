from Game.Board import Board
import random

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
        print(self.board.generateFenForBoard())
        print("moved")

    def opponentsMove(self, move):
        self.board.move(move)
        print(self.board.generateFenForBoard())
        print("opponent moved")

    def calculateBestMove(self, forWhite, depth, board=False):
        if not board:
            board = self.board
        moves = board.generatePossibleMoves(forWhite)
        if depth == 0:
            moves.sort(key = self.getMaterialDifferenceForMove, reverse = forWhite)
            return (moves[0], self.getMaterialDifferenceForMove(moves[0]))
        for move in moves:
            boardKey = board.testMove(move)
            bestMove = self.calculateBestMove(not forWhite, depth - 1, board.testBoards[boardKey])
            moves[moves.index(move)] = (moves[moves.index(move)], bestMove[1])
            self.board.popTestBoard(boardKey)
        moves.sort(key = lambda x: x[1], reverse = forWhite)
        return moves[0]

    def getMaterialDifferenceForMove(self, move, board=False):
        if not board:
            board = self.board
        boardKey = board.testMove(move)
        materialDifference = board.testBoards[boardKey].calculateMaterialDifference()
        return materialDifference
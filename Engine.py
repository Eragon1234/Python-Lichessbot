from Game.Board import Board
import random

class Engine:
    """
    Class to generate the best possible moves etc.
    """

    def __init__(self, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = Board(fen)

    def move(self, gameId, color, moves, moveFn):
        """ generates the best possible move

        Args:
            gameId (string): the id of the game to move in
            color (string): the color for whom to generate the best moves
            moves (string): moves since the start position
            moveFn (fn): function to make the move
        """
        forWhite = color == 'white'
        moves = self.board.generatePossibleMoves(forWhite)
        move = moves[random.randint(0, (len(moves) - 1))]
        print(move)
        self.board.move(move)
        moveFn(gameId, move)
        print(self.board.generateFenForBoard())
        print("moved")

    def opponentsMove(self, move):
        self.board.move(move)
        print(self.board.generateFenForBoard())
        print("opponent moved")

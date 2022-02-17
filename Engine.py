from Game.Board import Board
import random

class Engine:

    def __init__(self, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = Board(fen)

    def move(self, gameId, color, moves, moveFn):
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

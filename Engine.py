from Game.Board import Board
import random

class Engine:

    def __init__(self):
        self.board = Board()

    def move(self, gameId, color, moves, moveFn):
        forWhite = color == 'white'
        moves = self.board.generatePossibleMoves(forWhite)
        move = moves[random.randint(0, (len(moves) - 1))]
        print(move)
        self.board.move(move)
        print("moved")
        moveFn(gameId, move)
        print(self.board.generateFenForBoard())

    def opponentsMove(self, move):
        print("opponent moved")
        self.board.move(move)
        print(self.board.generateFenForBoard())

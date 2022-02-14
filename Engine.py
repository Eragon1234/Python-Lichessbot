from Game.Board import Board
import random

class Engine:

    def __init__(self):
        self.board = Board()

    def move(self, gameId, color, moves, moveFn):
        forWhite = color == 'white'
        moves = self.board.generatePossibleMoves(forWhite)
        print(moves)
        move = moves[random.randint(0, (len(moves) - 1))]
        print(move)
        moveFn(gameId, move)

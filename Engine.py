from Game.Board import Board
import random

class Engine:

    def __init__(self):
        self.board = Board()

    def move(self, gameId, moves, moveFn):
        moves = self.board.generatePossibleMoves()
        moveFn(gameId, moves[random.randint(0, len(moves))])

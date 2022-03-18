import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.board import Board

board = Board()

testMoveTimer = Timer("board.test_move('e2e4')", "from game.Board import Board; board=Board()", globals=globals())
print("Time test_move:", testMoveTimer.timeit(number=100) / 100)

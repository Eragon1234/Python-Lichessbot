import os
import sys
sys.path.append(os.getcwd())

from timeit import Timer
from Game.Board import Board
board = Board()

testMoveTimer = Timer("board.test_move('e2e4')", "from Game.Board import Board; board=Board()", globals=globals())
print("Time test_move:", testMoveTimer.timeit(number=10000) / 10000)
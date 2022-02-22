import os
import sys
sys.path.append(os.getcwd())

from timeit import Timer
from Game.Board import Board
board = Board()

calculateMaterialDifferenceTimer = Timer(board.calculateMaterialDifference)
print("Time calculateMaterialDifference:", calculateMaterialDifferenceTimer.timeit(number=10000) / 10000)
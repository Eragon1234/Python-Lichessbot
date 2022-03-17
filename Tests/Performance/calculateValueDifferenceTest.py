import os
import sys
sys.path.append(os.getcwd())

from timeit import Timer
from Game.Board import Board
board = Board()

calculateMaterialDifferenceTimer = Timer(board.calculate_value_difference)
print("Time calculate_material_difference:", calculateMaterialDifferenceTimer.timeit(number=100) / 100)
import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from Game.Board import Board

board = Board()

moveGenerationTimer = Timer(board.generate_possible_moves)
print("Time generate_possible_moves:", moveGenerationTimer.timeit(number=100) / 100)

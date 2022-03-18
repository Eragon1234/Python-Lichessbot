import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.pieces import Pawn

pawn = Pawn()

generateColorBoardTimer = Timer(pawn.generate_possible_positions)
print("Time generate_color_board:", generateColorBoardTimer.timeit(number=100) / 100)

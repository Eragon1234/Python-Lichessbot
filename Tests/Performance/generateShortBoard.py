import os
import sys
sys.path.append(os.getcwd())

from timeit import Timer
from Game.Board import Board
board = Board()

generateColorBoardTimer = Timer(board.generate_short_board)
print("Time generate_color_board:", generateColorBoardTimer.timeit(number=10000) / 10000)
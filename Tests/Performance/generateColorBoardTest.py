import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.board import Board

board = Board()

generateColorBoardTimer = Timer(board.generate_color_board)
print("Time generate_color_board:", generateColorBoardTimer.timeit(number=10) / 10)

import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.pieces import Rook
from game.board import Board

board = Board()
color_board = board.generate_color_board()
rook = Rook(True)

generatePossiblePositionsTimer = Timer("rook.generate_possible_positions((4,4), color_board)", globals=globals())
print("Time rook.generate_possible_positions:", generatePossiblePositionsTimer.timeit(number=100) / 100)

import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.pieces import Queen
from game.board import Board

board = Board()
color_board = board.generate_color_board()
queen = Queen(True)

generatePossiblePositionsTimer = Timer("queen.generate_possible_coordinate_moves((4,4), color_board)", globals=globals())
print("Time queen.generate_possible_coordinate_moves:", generatePossiblePositionsTimer.timeit(number=100) / 100)

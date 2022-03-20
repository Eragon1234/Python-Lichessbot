import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.pieces import Knight
from game.board import Board

board = Board()
color_board = board.generate_color_board()
knight = Knight(True)

generatePossiblePositionsTimer = Timer("knight.generate_possible_coordinate_moves((4,4), color_board)", globals=globals())
print("Time knight.generate_possible_coordinate_moves:", generatePossiblePositionsTimer.timeit(number=100) / 100)

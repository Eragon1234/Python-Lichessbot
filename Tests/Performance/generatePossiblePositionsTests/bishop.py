import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.pieces import Bishop
from game.board import Board

board = Board()
color_board = board.generate_color_board()
bishop = Bishop(True)

generatePossiblePositionsTimer = Timer("bishop.generate_possible_positions((4,4), color_board)", globals=globals())
print("Time bishop.generate_possible_positions:", generatePossiblePositionsTimer.timeit(number=100) / 100)

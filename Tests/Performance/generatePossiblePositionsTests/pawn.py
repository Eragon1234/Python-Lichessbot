import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.pieces import Pawn
from game.board import Board

board = Board()
color_board = board.generate_color_board()
pawn = Pawn(True)

generatePossiblePositionsTimer = Timer("pawn.generate_possible_positions((4,4), color_board)", globals=globals())
print("Time pawn.generate_possible_positions:", generatePossiblePositionsTimer.timeit(number=100) / 100)

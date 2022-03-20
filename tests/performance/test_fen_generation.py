import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from game.board import Board

board = Board()

generateFenForBoardTimer = Timer(board.generate_fen_for_board)
print("Time generate_fen_for_board:", generateFenForBoardTimer.timeit(number=100) / 100)

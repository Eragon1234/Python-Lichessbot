import os
import sys
sys.path.append(os.getcwd())

from timeit import Timer
from Game.Board import Board
board = Board()

generateFenForBoardTimer = Timer(board.generateFenForBoard)
print("Time generateFenForBoard:", generateFenForBoardTimer.timeit(number=10000) / 10000)
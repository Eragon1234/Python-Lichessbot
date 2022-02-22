from timeit import Timer
from Game.Board import Board
board = Board()

generateColorBoardTimer = Timer(board.generateColorBoard)
print("Time generateColorBoard:", generateColorBoardTimer.timeit(number=10000) / 10000)
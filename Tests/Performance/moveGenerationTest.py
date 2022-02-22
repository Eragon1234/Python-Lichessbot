from timeit import Timer
from Game.Board import Board
board = Board()

moveGenerationTimer = Timer(board.generatePossibleMoves)
print("Time generatePossibleMoves:", moveGenerationTimer.timeit(number=10000) / 10000)
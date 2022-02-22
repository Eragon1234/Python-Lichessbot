from timeit import Timer
from Game.Board import Board
board = Board()

testMoveTimer = Timer("board.testMove('e2e4')", "from Game.Board import Board; board=Board()", globals=globals())
print("Time testMove:", testMoveTimer.timeit(number=10000) / 10000)
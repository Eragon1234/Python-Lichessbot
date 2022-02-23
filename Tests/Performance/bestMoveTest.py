import os, sys
sys.path.append(os.getcwd())

from timeit import Timer
from Engine import Engine

engine = Engine()
bestMoveTime = Timer("engine.calculateBestMove(True, 4)", setup="from Engine import Engine; engine=Engine()")
print("Timer bestMoveCalculation", bestMoveTime.timeit(number=10) / 10)
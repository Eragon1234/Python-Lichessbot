import os, sys
sys.path.append(os.getcwd())

from timeit import Timer
from Engine import Engine

engine = Engine()
bestMoveTime = Timer("engine.calculate_best_move(True, 2)", setup="from Engine import Engine; engine=Engine()")
print("Timer bestMoveCalculation", bestMoveTime.timeit(number=10) / 10)
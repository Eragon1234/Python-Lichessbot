import os
import sys

sys.path.append(os.getcwd())

from timeit import Timer
from engine import Engine

engine = Engine()
bestMoveTime = Timer("engine.calculate_best_move(True, 2)", setup="from engine import Engine; engine=Engine()")
print("Timer bestMoveCalculation", bestMoveTime.timeit(number=10) / 10)

# TODO: refactoring the tests into unittests and optimize and clean them up

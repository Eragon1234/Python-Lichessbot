import unittest
from timeit import Timer

from engine import Engine
from playercolor import PlayerColor


class TestBestMoveGenerationPerformance(unittest.TestCase):
    repeat_runs = 5

    def setUp(self):
        self.engine = Engine()

    def test_check_performance_of_move_generation_with_depth_1(self):
        best_move_generation_time = self.run_with_depth(1)
        print("depth 1:", best_move_generation_time)
        self.assertLess(best_move_generation_time, 0.0125)

    def test_check_performance_of_move_generation_with_depth_2(self):
        best_move_generation_time = self.run_with_depth(2)
        print("depth 2:", best_move_generation_time)
        self.assertLess(best_move_generation_time, 0.025)

    def test_check_performance_of_move_generation_with_depth_3(self):
        best_move_generation_time = self.run_with_depth(3)
        print("depth 3:", best_move_generation_time)
        self.assertLess(best_move_generation_time, .05)

    def test_check_performance_of_move_generation_with_depth_4(self):
        best_move_generation_time = self.run_with_depth(4)
        print("depth 4:", best_move_generation_time)
        self.assertLess(best_move_generation_time, .1)

    def test_check_performance_of_move_generation_with_depth_5(self):
        best_move_generation_time = self.run_with_depth(5)
        print("depth 5:", best_move_generation_time)
        self.assertLess(best_move_generation_time, .3)

    def run_with_depth(self, depth: int) -> float:
        def run():
            self.engine.calculate_best_move(PlayerColor.White, depth)

        timer = Timer(run)
        return min(timer.repeat(repeat=self.repeat_runs, number=1))

import unittest
from timeit import Timer

from engine import Engine


class BestMoveGenerationPerformanceTests(unittest.TestCase):
    number_of_times_to_run_tests = 10

    def setUp(self):
        self.engine = Engine()

    def test_check_performance_of_move_generation_with_depth_1(self):
        best_move_generation_time = self.run_and_create_timer_with_depth(1)
        self.assertLess(best_move_generation_time, 0.1)

    def test_check_performance_of_move_generation_with_depth_2(self):
        best_move_generation_time = self.run_and_create_timer_with_depth(2)
        self.assertLess(best_move_generation_time, 1)

    def test_check_performance_of_move_generation_with_depth_3(self):
        best_move_generation_time = self.run_and_create_timer_with_depth(3)
        self.assertLess(best_move_generation_time, 5)

    def run_and_create_timer_with_depth(self, depth):
        timer = self.create_timer_with_depth(depth)
        return self.run_timer(timer)

    def create_timer_with_depth(self, depth):
        return Timer(f"engine.calculate_best_move(True, {depth})", globals={'engine': self.engine})

    def run_timer(self, timer):
        return timer.timeit(number=self.number_of_times_to_run_tests) / self.number_of_times_to_run_tests

import unittest
from timeit import Timer

from game.board import Board


class ValueDifferenceCalculationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_value_difference_calculation_time(self):
        calculate_material_difference_timer = Timer(self.board.calculate_value_difference)
        calculate_material_difference_time = calculate_material_difference_timer.timeit(number=100) / 100
        self.assertLess(calculate_material_difference_time, 0.01)

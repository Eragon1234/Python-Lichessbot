import unittest
from timeit import Timer

from game.board import Board


class ColorBoardGenerationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_performance_of_color_board_generation(self):
        color_board_generation_timer = Timer(self.board.generate_color_board)
        color_board_generation_time = color_board_generation_timer.timeit(number=10) / 10
        self.assertLess(color_board_generation_time, 0.01)

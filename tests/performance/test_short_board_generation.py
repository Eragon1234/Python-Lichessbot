import unittest
from timeit import Timer

from game.board import Board


class ShortBoardGenerationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_performance_of_the_short_board_generation(self):
        short_board_generation_timer = Timer(self.board.generate_short_board)
        short_board_generation_time = short_board_generation_timer.timeit(number=100) / 100
        self.assertLess(short_board_generation_time, 0.01)

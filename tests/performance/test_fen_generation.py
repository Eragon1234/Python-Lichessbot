import unittest
from timeit import Timer

from game.board import Board


class FenGenerationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_performance_of_fen_generation(self):
        fen_generation_timer = Timer(self.board.generate_fen_for_board)
        fen_generation_time = fen_generation_timer.timeit(number=100) / 100
        self.assertLess(fen_generation_time, 0.1)

import unittest
from timeit import Timer

from game.board import Board


class MoveGenerationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_performance_of_move_generation(self):
        move_generation_timer = Timer(self.board.generate_possible_moves)
        move_generation_time = move_generation_timer.timeit(number=100) / 100
        self.assertLess(move_generation_time, 0.1)

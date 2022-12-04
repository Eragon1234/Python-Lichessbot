import unittest
from timeit import Timer

from game import Board
from game import King


class KingPossiblePositionsGenerationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.king = King(True)
        self.color_board = Board().generate_color_board()

    def test_performance_of_possible_position_generation_of_the_king(self):
        possible_positions_generation_timer = Timer(
            f"king.generate_possible_positions((4,4), {self.color_board})", globals={'king': self.king})
        possible_positions_generation_time = possible_positions_generation_timer.timeit(number=100) / 100
        self.assertLess(possible_positions_generation_time, 0.01)

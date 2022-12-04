import unittest
from timeit import Timer

from game import Board
from game import Queen


class QueenPossiblePositionsGenerationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.queen = Queen(True)
        self.color_board = Board().generate_color_board()

    def test_performance_of_possible_position_generation_of_the_queen(self):
        possible_positions_generation_timer = Timer(
            f"queen.generate_possible_positions((4,4), {self.color_board})", globals={'queen': self.queen})
        possible_positions_generation_time = possible_positions_generation_timer.timeit(number=100) / 100
        self.assertLess(possible_positions_generation_time, 0.01)

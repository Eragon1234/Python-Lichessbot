import unittest
from timeit import Timer

from game import Pawn
from game import Board


class PawnPossiblePositionsGenerationPerformanceTest(unittest.TestCase):

    def setUp(self):
        self.pawn = Pawn(True)
        self.color_board = Board().generate_color_board()

    def test_performance_of_possible_position_generation_of_the_pawn(self):
        possible_positions_generation_timer = Timer(
            f"pawn.generate_possible_positions((4,4), {self.color_board})", globals={'pawn': self.pawn})
        possible_positions_generation_time = possible_positions_generation_timer.timeit(number=100) / 100
        self.assertLess(possible_positions_generation_time, 0.01)

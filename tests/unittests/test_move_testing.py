import sys, os

sys.path.append(os.getcwd())

import unittest
from game import Board


class MoveTestingTests(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_samePositionAfterTestingAllMovesInStartPosition(self):
        self.check_all_moves_and_check_for_equality_before_and_after()

    def test_correctPositionAfterTestingAllMovesInPositionWithCapturing(self):
        self.board.load_board_with_fen('rnbq1rk1/pp2ppbp/3p1np1/2p5/2PP4/2NBPN2/PP3PPP/R1BQK2R w KQ - 0 7')
        self.check_all_moves_and_check_for_equality_before_and_after()

    def test_correctPositionAfterTestingAllMovesInPositionWithCheck(self):
        self.board.load_board_with_fen('r5k1/5pp1/4p3/7Q/p1p3P1/P1B1q3/1P5P/5RK1 w - - 3 35')
        self.check_all_moves_and_check_for_equality_before_and_after()

    def check_all_moves_and_check_for_equality_before_and_after(self):
        moves = self.board.generate_possible_moves(True)
        for move in moves:
            start_board = self.board.generate_short_board()
            with self.board.test_move(move) as board:
                board.generate_short_board()
            end_board = self.board.generate_short_board()

            self.assertCountEqual(start_board, end_board)

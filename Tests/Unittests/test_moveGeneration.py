import os, sys

sys.path.append(os.getcwd())
import unittest


class TestMoveGeneration(unittest.TestCase):

    def setUp(self):
        from Game.Board import Board
        self.board = Board()

    def test_correctNumberOfMovesInStartPosition(self):
        moves = self.board.generate_possible_moves(True)
        self.assertEqual(len(moves), 20)

    def test_correctNumberOfMovesInExamplePosition1(self):
        self.board.load_board_with_fen('r2q1rk1/p2n1pp1/1p2pn1p/8/1P1Nb3/2BBP3/1PQ2P1P/3RK1R1 b - - 3 16')
        moves = self.board.generate_possible_moves(False)
        self.assertEqual(len(moves), 35)

    def test_correctNumberOfMovesInExamplePosition2(self):
        self.board.load_board_with_fen('r5r1/p4N1k/1p2p1pp/1P6/1q5P/3nPQ2/1P1RK3/6R1 b - - 5 30')
        moves = self.board.generate_possible_moves(False)
        self.assertEqual(len(moves), 43)

    def test_correctNumberOfMovesInExamplePosition3(self):
        self.board.load_board_with_fen('r6k/1q3pp1/4p3/8/p1pr1P2/P2n4/1PQB2PP/1R3RK1 w - - 0 26')
        moves = self.board.generate_possible_moves(True)
        self.assertEqual(len(moves), 30)

    def test_correctNumberOfMovesInExamplePosition4(self):
        self.board.load_board_with_fen('4r3/1pP1N1k1/2br1p1p/p1p1nP2/2PpP1P1/8/PP2B3/3R1K1R b - - 1 32')
        moves = self.board.generate_possible_moves(False)
        self.assertEqual(len(moves), 33)

    def test_correctNumberOfMovesInExamplePositionWithCheck(self):
        self.board.load_board_with_fen('r5k1/5pp1/4p3/7Q/p1p3P1/P1B1q3/1P5P/5RK1 w - - 3 35')
        moves = self.board.generate_possible_moves(True)
        self.assertEqual(len(moves), 3)

    def test_correctNumberOfMovesInExamplePositionWithEnPassant(self):
        self.board.load_board_with_fen('r1b1k2r/2q1bppp/p1nppn2/Pp6/4PP2/1NNB4/1PP3PP/R1BQ1RK1 w kq b6 0 12')
        moves = self.board.generate_possible_moves(True)
        self.assertEqual(len(moves), 36)

    def test_correctNumberOfMovesInExamplePositionWithCastling(self):
        self.board.load_board_with_fen('r3k2r/ppp2ppp/3p1q2/6b1/2P1P3/2NQ3P/PPP3P1/R3K2R b KQkq - 4 15')
        moves = self.board.generate_possible_moves(False)
        self.assertEqual(len(moves), 40)

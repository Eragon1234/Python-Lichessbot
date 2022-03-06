import os, sys
sys.path.append(os.getcwd())
import unittest

class TestMoveGeneration(unittest.TestCase):

    def setUp(self):
        from Game.Board import Board
        self.board = Board()

    def test_correctNumberOfMovesInStartPosition(self):
        self.assertEqual(len(self.board.generate_possible_moves(True)), 20)

    def test_correctNumberOfMovesInExamplePosition1(self):
        self.board.load_board_with_fen('r2q1rk1/p2n1pp1/1p2pn1p/8/1P1Nb3/2BBP3/1PQ2P1P/3RK1R1 b - - 3 16')
        self.assertEqual(len(self.board.generate_possible_moves(False)), 35)
    
    def test_correctNumberOfMovesInExamplePosition2(self):
        self.board.load_board_with_fen('r5r1/p4N1k/1p2p1pp/1P6/1q5P/3nPQ2/1P1RK3/6R1 b - - 5 30')
        self.assertEqual(len(self.board.generate_possible_moves(False)), 43)

    def test_correctNumberOfMovesInExamplePosition3(self):
        self.board.load_board_with_fen('r6k/1q3pp1/4p3/8/p1pr1P2/P2n4/1PQB2PP/1R3RK1 w - - 0 26')
        self.assertEqual(len(self.board.generate_possible_moves(True)), 30)

    def test_correctNumberOfMovesInExamplePositionWithCheck(self):
        self.board.load_board_with_fen('r5k1/5pp1/4p3/7Q/p1p3P1/P1B1q3/1P5P/5RK1 w - - 3 35')
        self.assertEqual(len(self.board.generate_possible_moves(True)), 3)

    def test_correctNumberOfMovesInExamplePositionWithEnPassant(self):
        self.board.load_board_with_fen('r1b1k2r/2q1bppp/p1nppn2/Pp6/4PP2/1NNB4/1PP3PP/R1BQ1RK1 w kq b6 0 12')
        self.assertEqual(len(self.board.generate_possible_moves(True)), 36)

    def test_correctNumberOfMovesInExamplePositionWithCastling(self):
        self.board.load_board_with_fen('r3k2r/ppp2ppp/3p1q2/6b1/2P1P3/2NQ3P/PPP3P1/R3K2R b KQkq - 4 15')
        self.assertEqual(len(self.board.generate_possible_moves(False)), 40)
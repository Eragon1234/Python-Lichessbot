import os, sys

sys.path.append(os.getcwd())
import unittest


class TestMoveGeneration(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        from Game.Board import Board
        self.board = Board()

    def test_correctMovesInStartPosition(self):
        moves = self.board.generate_possible_moves(True)
        stockfish_moves = ['a2a3', 'b2b3', 'c2c3', 'd2d3', 'e2e3', 'f2f3', 'g2g3', 'h2h3', 'a2a4', 'b2b4', 'c2c4',
                           'd2d4', 'e2e4', 'f2f4', 'g2g4', 'h2h4', 'b1a3', 'b1c3', 'g1f3', 'g1h3']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPosition1(self):
        self.board.load_board_with_fen('r2q1rk1/p2n1pp1/1p2pn1p/8/1P1Nb3/2BBP3/1PQ2P1P/3RK1R1 b - - 3 16')
        moves = self.board.generate_possible_moves(False)
        stockfish_moves = ['b6b5', 'e6e5', 'h6h5', 'a7a6', 'g7g6', 'a7a5', 'g7g5', 'f6g4', 'f6d5', 'f6h5', 'f6h7',
                           'f6e8', 'd7c5', 'd7e5', 'd7b8', 'e4h1', 'e4g2', 'e4d3', 'e4f3', 'e4d5', 'e4f5', 'e4c6',
                           'e4g6', 'e4b7', 'e4h7', 'a8b8', 'a8c8', 'f8e8', 'd8c7', 'd8e7', 'd8b8', 'd8c8', 'd8e8',
                           'g8h7', 'g8h8']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPosition2(self):
        self.board.load_board_with_fen('r5r1/p4N1k/1p2p1pp/1P6/1q5P/3nPQ2/1P1RK3/6R1 b - - 5 30')
        moves = self.board.generate_possible_moves(False)
        stockfish_moves = ['e6e5', 'g6g5', 'h6h5', 'a7a6', 'a7a5', 'd3c1', 'd3e1', 'd3b2', 'd3f2', 'd3f4', 'd3c5',
                           'd3e5', 'a8b8', 'a8c8', 'a8d8', 'a8e8', 'a8f8', 'g8g7', 'g8b8', 'g8c8', 'g8d8', 'g8e8',
                           'g8f8', 'g8h8', 'b4b2', 'b4d2', 'b4a3', 'b4b3', 'b4c3', 'b4a4', 'b4c4', 'b4d4', 'b4e4',
                           'b4f4', 'b4g4', 'b4h4', 'b4a5', 'b4b5', 'b4c5', 'b4d6', 'b4e7', 'b4f8', 'h7g7']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPosition3(self):
        self.board.load_board_with_fen('r6k/1q3pp1/4p3/8/p1pr1P2/P2n4/1PQB2PP/1R3RK1 w - - 0 26')
        moves = self.board.generate_possible_moves(True)
        stockfish_moves = ['b2b3', 'g2g3', 'h2h3', 'f4f5', 'b2b4', 'g2g4', 'h2h4', 'd2c1', 'd2e1', 'd2c3', 'd2e3',
                           'd2b4', 'd2a5', 'b1a1', 'b1c1', 'b1d1', 'b1e1', 'f1c1', 'f1d1', 'f1e1', 'f1f2', 'f1f3',
                           'c2c1', 'c2d1', 'c2b3', 'c2c3', 'c2d3', 'c2a4', 'c2c4', 'g1h1']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPosition4(self):
        self.board.load_board_with_fen('4r3/1pP1N1k1/2br1p1p/p1p1nP2/2PpP1P1/8/PP2B3/3R1K1R b - - 1 32')
        moves = self.board.generate_possible_moves(False)
        stockfish_moves = ['d4d3', 'a5a4', 'h6h5', 'b7b6', 'b7b5', 'e5d3', 'e5f3', 'e5c4', 'e5g4', 'e5g6', 'e5d7',
                           'e5f7', 'c6a4', 'c6e4', 'c6b5', 'c6d5', 'c6d7', 'd6d5', 'd6e6', 'd6d7', 'd6d8', 'e8e7',
                           'e8a8', 'e8b8', 'e8c8', 'e8d8', 'e8f8', 'e8g8', 'e8h8', 'g7h8', 'g7f7', 'g7h7', 'g7f8']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPosition5(self):
        self.board.load_board_with_fen('5k2/1p6/p3b1Q1/4p1B1/4p3/PN1B2P1/1PP2q1P/7K w - - 0 27')
        moves = self.board.generate_possible_moves(True)
        stockfish_moves = ['c2c3', 'h2h3', 'a3a4', 'g3g4', 'c2c4', 'h2h4', 'b3a1', 'b3c1', 'b3d2', 'b3d4', 'b3a5',
                           'b3c5', 'd3f1', 'd3e2', 'd3c4', 'd3e4', 'd3b5', 'd3a6', 'g5c1', 'g5d2', 'g5e3', 'g5f4',
                           'g5h4', 'g5f6', 'g5h6', 'g5e7', 'g5d8', 'g6e4', 'g6f5', 'g6h5', 'g6e6', 'g6f6', 'g6h6',
                           'g6f7', 'g6g7', 'g6h7', 'g6e8', 'g6g8']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPositionWithCheck1(self):
        self.board.load_board_with_fen('r5k1/5pp1/4p3/7Q/p1p3P1/P1B1q3/1P5P/5RK1 w - - 3 35')
        moves = self.board.generate_possible_moves(True)
        stockfish_moves = ['f1f2', 'g1h1', 'g1g2']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPositionWithCheck2(self):
        self.board.load_board_with_fen('r4rk1/3RN1pp/p4p2/1p6/6P1/7P/PnP5/5RK1 b - - 1 25')
        moves = self.board.generate_possible_moves(False)
        stockfish_moves = ['g8f7', 'g8h8']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPositionWithEnPassant(self):
        self.board.load_board_with_fen('r1b1k2r/2q1bppp/p1nppn2/Pp6/4PP2/1NNB4/1PP3PP/R1BQ1RK1 w kq b6 0 12')
        moves = self.board.generate_possible_moves(True)
        stockfish_moves = ['g2g3', 'h2h3', 'e4e5', 'f4f5', 'g2g4', 'h2h4', 'a5b6', 'b3d2', 'b3d4', 'b3c5', 'c3b1',
                           'c3a2', 'c3e2', 'c3a4', 'c3b5', 'c3d5', 'c1d2', 'c1e3', 'd3e2', 'd3c4', 'd3b5', 'a1b1',
                           'a1a2', 'a1a3', 'a1a4', 'f1e1', 'f1f2', 'f1f3', 'd1e1', 'd1d2', 'd1e2', 'd1f3', 'd1g4',
                           'd1h5', 'g1h1', 'g1f2']
        self.assertCountEqual(moves, stockfish_moves)

    def test_correctMovesInTestPositionWithCastling(self):
        self.board.load_board_with_fen('r3k2r/ppp2ppp/3p1q2/6b1/2P1P3/2NQ3P/PPP3P1/R3K2R b KQkq - 4 15')
        moves = self.board.generate_possible_moves(False)
        stockfish_moves = ['d6d5', 'a7a6', 'b7b6', 'c7c6', 'g7g6', 'h7h6', 'a7a5', 'b7b5', 'c7c5', 'h7h5', 'g5c1',
                           'g5d2', 'g5e3', 'g5f4', 'g5h4', 'g5h6', 'a8b8', 'a8c8', 'a8d8', 'h8f8', 'h8g8', 'f6f1',
                           'f6f2', 'f6c3', 'f6f3', 'f6d4', 'f6f4', 'f6e5', 'f6f5', 'f6e6', 'f6g6', 'f6h6', 'f6e7',
                           'f6d8', 'e8d7', 'e8e7', 'e8d8', 'e8f8', 'e8g8', 'e8c8']
        self.assertCountEqual(moves, stockfish_moves)

import unittest

from game import ChessBoard


class TestMoveGeneration(unittest.TestCase):
    maxDiff = None

    def test_move_generation(self):
        test_cases: dict[str, Case] = {
            "start position": Case(
                'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                ['a2a3', 'b2b3', 'c2c3', 'd2d3', 'e2e3', 'f2f3', 'g2g3',
                 'h2h3', 'a2a4', 'b2b4', 'c2c4', 'd2d4', 'e2e4', 'f2f4',
                 'g2g4', 'h2h4', 'b1a3', 'b1c3', 'g1f3', 'g1h3']),
            "test position 1": Case(
                'r2q1rk1/p2n1pp1/1p2pn1p/8/1P1Nb3/2BBP3/1PQ2P1P/3RK1R1 b - - 3 16',
                ['b6b5', 'e6e5', 'h6h5', 'a7a6', 'g7g6', 'a7a5', 'g7g5',
                 'f6g4', 'f6d5', 'f6h5', 'f6h7', 'f6e8', 'd7c5', 'd7e5',
                 'd7b8', 'e4h1', 'e4g2', 'e4d3', 'e4f3', 'e4d5', 'e4f5',
                 'e4c6', 'e4g6', 'e4b7', 'e4h7', 'a8b8', 'a8c8', 'f8e8',
                 'd8c7', 'd8e7', 'd8b8', 'd8c8', 'd8e8', 'g8h7', 'g8h8']),
            "test position 2": Case(
                'r5r1/p4N1k/1p2p1pp/1P6/1q5P/3nPQ2/1P1RK3/6R1 b - - 5 30',
                ['e6e5', 'g6g5', 'h6h5', 'a7a6', 'a7a5', 'd3c1', 'd3e1',
                 'd3b2', 'd3f2', 'd3f4', 'd3c5', 'd3e5', 'a8b8', 'a8c8',
                 'a8d8', 'a8e8', 'a8f8', 'g8g7', 'g8b8', 'g8c8', 'g8d8',
                 'g8e8', 'g8f8', 'g8h8', 'b4b2', 'b4d2', 'b4a3', 'b4b3',
                 'b4c3', 'b4a4', 'b4c4', 'b4d4', 'b4e4', 'b4f4', 'b4g4',
                 'b4h4', 'b4a5', 'b4b5', 'b4c5', 'b4d6', 'b4e7', 'b4f8',
                 'h7g7']),
            "test position 3": Case(
                'r6k/1q3pp1/4p3/8/p1pr1P2/P2n4/1PQB2PP/1R3RK1 w - - 0 26',
                ['b2b3', 'g2g3', 'h2h3', 'f4f5', 'b2b4', 'g2g4', 'h2h4',
                 'd2c1', 'd2e1', 'd2c3', 'd2e3', 'd2b4', 'd2a5', 'b1a1',
                 'b1c1', 'b1d1', 'b1e1', 'f1c1', 'f1d1', 'f1e1', 'f1f2',
                 'f1f3', 'c2c1', 'c2d1', 'c2b3', 'c2c3', 'c2d3', 'c2a4',
                 'c2c4', 'g1h1']),
            "test position 4": Case(
                '4r3/1pP1N1k1/2br1p1p/p1p1nP2/2PpP1P1/8/PP2B3/3R1K1R b - - 1 32',
                ['d4d3', 'a5a4', 'h6h5', 'b7b6', 'b7b5', 'e5d3', 'e5f3',
                 'e5c4', 'e5g4', 'e5g6', 'e5d7', 'e5f7', 'c6a4', 'c6e4',
                 'c6b5', 'c6d5', 'c6d7', 'd6d5', 'd6e6', 'd6d7', 'd6d8',
                 'e8e7', 'e8a8', 'e8b8', 'e8c8', 'e8d8', 'e8f8', 'e8g8',
                 'e8h8', 'g7h8', 'g7f7', 'g7h7', 'g7f8']),
            "test position 5": Case(
                '5k2/1p6/p3b1Q1/4p1B1/4p3/PN1B2P1/1PP2q1P/7K w - - 0 27',
                ['c2c3', 'h2h3', 'a3a4', 'g3g4', 'c2c4', 'h2h4', 'b3a1',
                 'b3c1', 'b3d2', 'b3d4', 'b3a5', 'b3c5', 'd3f1', 'd3e2',
                 'd3c4', 'd3e4', 'd3b5', 'd3a6', 'g5c1', 'g5d2', 'g5e3',
                 'g5f4', 'g5h4', 'g5f6', 'g5h6', 'g5e7', 'g5d8', 'g6e4',
                 'g6f5', 'g6h5', 'g6e6', 'g6f6', 'g6h6', 'g6f7', 'g6g7',
                 'g6h7', 'g6e8', 'g6g8']),
            "test position 6": Case('6kr/1q1r2qp/8/p7/K7/8/8/8 b - - 1 75',
                                    ['g8f8', 'g8f7', 'g7f8', 'g7f7', 'g7e7',
                                     'g7h6', 'g7g6',
                                     'g7f6', 'g7g5', 'g7e5', 'g7g4', 'g7d4',
                                     'g7g3', 'g7c3',
                                     'g7g2', 'g7b2', 'g7g1', 'g7a1', 'd7d8',
                                     'd7f7', 'd7e7',
                                     'd7c7', 'd7d6', 'd7d5', 'd7d4', 'd7d3',
                                     'd7d2', 'd7d1',
                                     'b7c8', 'b7b8', 'b7a8', 'b7c7', 'b7a7',
                                     'b7c6', 'b7b6',
                                     'b7a6', 'b7d5', 'b7b5', 'b7e4', 'b7b4',
                                     'b7f3', 'b7b3',
                                     'b7g2', 'b7b2', 'b7h1', 'b7b1', 'h7h6',
                                     'h7h5']),
            "position with check": Case(
                'r5k1/5pp1/4p3/7Q/p1p3P1/P1B1q3/1P5P/5RK1 w - - 3 35',
                ['f1f2', 'g1h1', 'g1g2']),
            "position with check 2": Case(
                'r4rk1/3RN1pp/p4p2/1p6/6P1/7P/PnP5/5RK1 b - - 1 25',
                ['g8f7', 'g8h8']),
            "position with check 3": Case(
                'r1b1kb1r/pp3ppp/2n1pn2/4q3/7P/P1PP1PP1/8/RNBQKBNR w KQkq - 1 11',
                ['e1f2', 'e1d2', 'g1e2', 'f1e2', 'd1e2', 'c1e3']),
            "position with en passant": Case(
                'r1b1k2r/2q1bppp/p1nppn2/Pp6/4PP2/1NNB4/1PP3PP/R1BQ1RK1 w kq b6 0 12',
                ['g2g3', 'h2h3', 'e4e5', 'f4f5', 'g2g4', 'h2h4', 'a5b6',
                 'b3d2', 'b3d4', 'b3c5', 'c3b1', 'c3a2', 'c3e2', 'c3a4',
                 'c3b5', 'c3d5', 'c1d2', 'c1e3', 'd3e2', 'd3c4', 'd3b5',
                 'a1b1', 'a1a2', 'a1a3', 'a1a4', 'f1e1', 'f1f2', 'f1f3',
                 'd1e1', 'd1d2', 'd1e2', 'd1f3', 'd1g4', 'd1h5', 'g1h1',
                 'g1f2']),
            "position with castling": Case(
                'r3k2r/ppp2ppp/3p1q2/6b1/2P1P3/2NQ3P/PPP3P1/R3K2R b KQkq - 4 15',
                ['d6d5', 'a7a6', 'b7b6', 'c7c6', 'g7g6', 'h7h6', 'a7a5',
                 'b7b5', 'c7c5', 'h7h5', 'g5c1', 'g5d2', 'g5e3', 'g5f4',
                 'g5h4', 'g5h6', 'a8b8', 'a8c8', 'a8d8', 'h8f8', 'h8g8',
                 'f6f1', 'f6f2', 'f6c3', 'f6f3', 'f6d4', 'f6f4', 'f6e5',
                 'f6f5', 'f6e6', 'f6g6', 'f6h6', 'f6e7', 'f6d8', 'e8d7',
                 'e8e7', 'e8d8', 'e8f8', 'e8g8', 'e8c8']),
            "position with pin": Case(
                'rnbq4/pp6/2p1P2k/4P2n/6P1/8/PPpN1P2/2K4R b - - 0 23',
                ['d8h8', 'd8g8', 'd8f8', 'd8e8', 'd8e7', 'd8d7', 'd8c7',
                 'd8f6', 'd8d6', 'd8b6', 'd8g5', 'd8d5', 'd8a5', 'd8h4',
                 'd8d4', 'd8d3', 'd8d2', 'c8d7', 'c8e6', 'b8d7', 'b8a6',
                 'h6h7', 'h6g7', 'h6g6', 'h6g5', 'b7b6', 'a7a6', 'c6c5',
                 'b7b5', 'a7a5'])
        }

        for name, case in test_cases.items():
            with self.subTest(name):
                board = ChessBoard(case.fen)
                moves = board.legal_moves()
                moves = [move.uci() for move in moves]
                self.assertCountEqual(case.expected, moves)


class Case:
    def __init__(self, fen: str, expected: list[str]):
        self.fen = fen
        self.expected = expected

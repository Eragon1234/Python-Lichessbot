import unittest

from game import ChessBoard


class TestFen(unittest.TestCase):
    def test_fen(self):
        test_fens: list[str] = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "6k1/3R4/8/5p2/8/1R6/3P1KP1/6N1 b - - 0 25",
            "2r3k1/ppN2ppp/2n1bp2/8/8/8/PPPP1KPP/R1B2BNR w - - 3 12"
        ]

        for fen in test_fens:
            with self.subTest(fen=fen):
                board = ChessBoard(fen)
                self.assertEqual(fen, board.fen())

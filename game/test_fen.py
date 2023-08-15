import unittest

from game import ChessBoard


class TestFen(unittest.TestCase):
    def test_fen(self):
        test_fens: list[str] = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        ]

        for fen in test_fens:
            board = ChessBoard(fen)
            self.assertEqual(fen, board.fen())

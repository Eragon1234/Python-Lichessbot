import unittest

from game import ChessBoard


class TestMove(unittest.TestCase):
    def test_move(self):
        test_cases: list[tuple[str, str, str]] = [
            (
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "g1h3",
                "rnbqkbnr/pppppppp/8/8/8/7N/PPPPPPPP/RNBQKB1R b KQkq - 1 1",
            ),
            (
                "r2qk2r/pp1n2pp/1b1pb3/1Pp1ppN1/2P1P3/P2P3P/5PP1/R1BQKB1R b KQkq - 1 13",
                "d8f6",
                "r3k2r/pp1n2pp/1b1pbq2/1Pp1ppN1/2P1P3/P2P3P/5PP1/R1BQKB1R w KQkq - 2 14"
            ),
            (
                "r1bqk2r/pppp1ppp/2n2n2/2b1p3/4P3/P2P1N1P/1PP2PP1/RNBQKB1R b KQkq - 0 5",
                "d7d6",
                "r1bqk2r/ppp2ppp/2np1n2/2b1p3/4P3/P2P1N1P/1PP2PP1/RNBQKB1R w KQkq - 0 6"
            ),
            (
                "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "e2e4",
                "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
            ),
            (
                "8/5pk1/4p1rp/1r6/8/5R2/2RK1p2/8 b - - 1 49",
                "f2f1q",
                "8/5pk1/4p1rp/1r6/8/5R2/2RK4/5q2 w - - 0 50"
            )
        ]

        for fen, move, expected_fen in test_cases:
            with self.subTest(fen=fen, move=move):
                board = ChessBoard(fen)
                board.move(move)
                self.assertEqual(board.fen(), expected_fen)

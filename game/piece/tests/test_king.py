from unittest import TestCase

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestKing(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "king in the corner": Case((0, 0), [
                (1, 0),
                (0, 1), (1, 1)
            ]),
            "all empty fields": Case((4, 4), [
                (3, 3), (4, 3), (5, 3),
                (3, 4), (5, 4),
                (3, 5), (4, 5), (5, 5)
            ]),
            "field occupied by own piece": Case((4, 4), [
                (3, 3), (4, 3), (5, 3),
                (5, 4),
                (3, 5), (4, 5), (5, 5)
            ]).with_piece(Color.WHITE, 3, 4),
            "field occupied by enemy piece": Case((4, 4), [
                (3, 3), (4, 3), (5, 3),
                (3, 4), (5, 4),
                (3, 5), (4, 5), (5, 5)
            ]).with_piece(Color.BLACK, 3, 4)
        }

        king = Piece(PieceType.KING, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = king.positions(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

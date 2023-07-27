from unittest import TestCase

from game.pieces import Piece
from game.pieces.color import Color
from game.pieces.piece_type import PieceType
from game.pieces.tests.case import Case


class TestRook(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "completely empty board": Case((4, 4), [
                (4, 5), (4, 6), (4, 7), (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4),
                (0, 4)
            ]),
            "field in front occupied by own piece": Case((4, 4), [
                (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4), (0, 4)
            ]).with_piece(Color.WHITE, 4, 5),
            "field in front occupied by enemy piece": Case((4, 4), [
                (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4), (0, 4), (4, 5)
            ]).with_piece(Color.BLACK, 4, 5),
        }

        rook = Piece(PieceType.ROOK, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = rook.generate_possible_positions(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

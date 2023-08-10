import unittest

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestKnight(unittest.TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty board": Case((4, 4), [
                (2, 3),
                (2, 5),
                (3, 2),
                (3, 6),
                (5, 2),
                (5, 6),
                (6, 3),
                (6, 5)
            ]),
            "target field occupied by own piece": Case((4, 4), [
                (2, 5),
                (3, 2),
                (3, 6),
                (5, 2),
                (5, 6),
                (6, 3),
                (6, 5)
            ]).with_piece(Color.WHITE, 2, 3),
            "target field occupied by enemy piece": Case((4, 4), [
                (2, 3),
                (2, 5),
                (3, 2),
                (3, 6),
                (5, 2),
                (5, 6),
                (6, 3),
                (6, 5)
            ]).with_piece(Color.BLACK, 2, 3),
            "positioned in the corner": Case((0, 0), [
                (1, 2),
                (2, 1)
            ]),
        }

        knight = Piece(PieceType.KNIGHT, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = knight.positions(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

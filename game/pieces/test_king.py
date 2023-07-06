from unittest import TestCase

from game import King
from game.pieces.test_case import Case


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
            ]).with_piece(True, 3, 4),
            "field occupied by enemy piece": Case((4, 4), [
                (3, 3), (4, 3), (5, 3),
                (3, 4), (5, 4),
                (3, 5), (4, 5), (5, 5)
            ]).with_piece(False, 3, 4)
        }

        king = King(True)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = king.generate_possible_positions(test_case.position, test_case.board)

                self.assertCountEqual(test_case.expected, actual)

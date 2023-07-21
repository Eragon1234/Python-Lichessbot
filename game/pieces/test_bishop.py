from unittest import TestCase

from game import Bishop
from game.pieces.test_case import Case


class TestBishop(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty_board": Case((4, 4), [
                (5, 5), (6, 6), (7, 7),
                (5, 3), (6, 2), (7, 1),
                (3, 5), (2, 6), (1, 7),
                (3, 3), (2, 2), (1, 1), (0, 0)
            ]),
            "field occupied by own piece": Case((4, 4), [
                (5, 3), (6, 2), (7, 1),
                (3, 5), (2, 6), (1, 7),
                (3, 3), (2, 2), (1, 1), (0, 0)
            ]).with_piece(True, 5, 5),
            "field occupied by enemy piece": Case((4, 4), [
                (5, 3), (6, 2), (7, 1),
                (3, 5), (2, 6), (1, 7),
                (3, 3), (2, 2), (1, 1), (0, 0),
                (5, 5)
            ]).with_piece(False, 5, 5),
        }

        bishop = Bishop(True)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = bishop.generate_possible_positions(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

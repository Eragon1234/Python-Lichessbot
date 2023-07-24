from unittest import TestCase

from game.pieces import Piece
from game.pieces.piece_type import PieceType
from game.pieces.test_case import Case


class TestQueen(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty board": Case((4, 4), [
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7),
                (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4),
                (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
                (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1)
            ]),
            "field occupied by own piece": Case((4, 4), [
                (4, 0), (4, 1), (4, 2), (4, 3),
                (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4),
                (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
                (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1)
            ]).with_piece(True, 4, 5),
            "field occupied by enemy piece": Case((4, 4), [
                (4, 0), (4, 1), (4, 2), (4, 3), (4, 5),
                (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4),
                (0, 0), (1, 1), (2, 2), (3, 3), (5, 5), (6, 6), (7, 7),
                (1, 7), (2, 6), (3, 5), (5, 3), (6, 2), (7, 1)
            ]).with_piece(False, 4, 5),
        }

        queen = Piece(PieceType.QUEEN, True)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = queen.generate_possible_positions(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

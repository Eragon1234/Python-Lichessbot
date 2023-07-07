from unittest import TestCase

from game import Pawn
from game.pieces.test_case import Case


class TestPawn(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty board": Case((4, 4), [
                (4, 5)
            ]),
            "field in front occupied by own piece": Case((4, 4), []).with_piece(True, 4, 5),
            "field in front occupied by enemy piece": Case((4, 4), []).with_piece(False, 4, 5),
            "field left front occupied by enemy piece": Case((4, 4), [
                (3, 5),
                (4, 5)
            ]).with_piece(False, 3, 5),
            "field right front occupied by enemy piece": Case((4, 4), [
                (5, 5),
                (4, 5)
            ]).with_piece(False, 5, 5),
            "field right front occupied by own piece": Case((4, 4), [
                (4, 5)
            ]).with_piece(True, 5, 5),
            "field left front occupied by own piece": Case((4, 4), [
                (4, 5)
            ]).with_piece(True, 3, 5),
            "possible enpassant": Case((4, 4), [
                (4, 5),
                (3, 5)
            ]).with_piece("enemy", 3, 5).with_piece(False, 3, 4)
        }

        pawn = Pawn(True)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = pawn.generate_possible_positions(test_case.position, test_case.board)

                self.assertCountEqual(test_case.expected, actual)

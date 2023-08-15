from unittest import TestCase

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestKing(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "king in the corner": Case("h1", ['g1', 'h2', 'g2']),
            "all empty fields": Case("d5", ['e4', 'd4', 'c4',
                                            'e5', 'c5', 'e6', 'd6', 'c6']),
            "field occupied by own piece": Case("d5", ['e4',
                                                       'd4', 'c4', 'c5', 'e6',
                                                       'd6', 'c6']).with_piece(
                Color.WHITE, "e5"),
            "field occupied by enemy piece": Case("d5", ['e4',
                                                         'd4', 'c4', 'e5',
                                                         'c5', 'e6', 'd6',
                                                         'c6']).with_piece(
                Color.BLACK, "e5")
        }

        king = Piece(PieceType.KING, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = king.moves(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

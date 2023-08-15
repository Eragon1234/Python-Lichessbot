from unittest import TestCase

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestBishop(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty_board": Case("d5", ['c6', 'b7', 'a8', 'c4',
                                       'b3', 'a2', 'e6', 'f7', 'g8', 'e4',
                                       'f3', 'g2', 'h1']),
            "field occupied by own piece": Case("d5", ['c4',
                                                       'b3', 'a2', 'e6', 'f7',
                                                       'g8', 'e4', 'f3', 'g2',
                                                       'h1']).with_piece(
                Color.WHITE, "c6"),
            "field occupied by enemy piece": Case("d5", ['c4',
                                                         'b3', 'a2', 'e6',
                                                         'f7', 'g8', 'e4',
                                                         'f3', 'g2', 'h1',
                                                         'c6']).with_piece(
                Color.BLACK, "c6"),
        }

        bishop = Piece(PieceType.BISHOP, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = bishop.moves(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

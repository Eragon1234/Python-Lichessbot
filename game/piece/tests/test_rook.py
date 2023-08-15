from unittest import TestCase

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestRook(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "completely empty board": Case(
                "d5", ['d6', 'd7', 'd8',
                       'd4', 'd3', 'd2', 'd1',
                       'c5', 'b5', 'a5', 'e5',
                       'f5', 'g5', 'h5']),
            "field in front occupied by own piece": Case(
                "d5", ['d4', 'd3', 'd2', 'd1', 'c5', 'b5', 'a5',
                       'e5', 'f5', 'g5', 'h5']).with_piece(Color.WHITE, "d6"),
            "field in front occupied by enemy piece": Case(
                "d5", ['d4', 'd3', 'd2', 'd1', 'c5', 'b5', 'a5',
                       'e5', 'f5', 'g5', 'h5', 'd6']).with_piece(Color.BLACK, "d6"),
        }

        rook = Piece(PieceType.ROOK, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = rook.moves(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

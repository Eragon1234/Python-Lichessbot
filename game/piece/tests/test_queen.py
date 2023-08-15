from unittest import TestCase

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestQueen(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty board": Case("d5", ['d1', 'd2', 'd3', 'd4',
                                       'd6', 'd7', 'd8', 'h5', 'g5', 'f5',
                                       'e5', 'c5', 'b5', 'a5', 'h1', 'g2',
                                       'f3', 'e4', 'c6', 'b7', 'a8', 'g8',
                                       'f7', 'e6', 'c4', 'b3', 'a2']),
            "field occupied by own piece": Case("d5", [
                'd1', 'd2', 'd3', 'd4', 'h5', 'g5', 'f5', 'e5', 'c5', 'b5',
                'a5', 'h1', 'g2', 'f3', 'e4', 'c6', 'b7', 'a8', 'g8', 'f7',
                'e6', 'c4', 'b3', 'a2'
            ]).with_piece(Color.WHITE, "d6"),
            "field occupied by enemy piece": Case("d5", [
                'd1', 'd2', 'd3', 'd4', 'd6', 'h5', 'g5', 'f5', 'e5', 'c5',
                'b5', 'a5', 'h1', 'g2', 'f3', 'e4', 'c6', 'b7', 'a8', 'g8',
                'f7', 'e6', 'c4', 'b3', 'a2'
            ]).with_piece(Color.BLACK, "d6"),
        }

        queen = Piece(PieceType.QUEEN, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = queen.moves(test_case.board, test_case.position)

                self.assertCountEqual(test_case.expected, actual)

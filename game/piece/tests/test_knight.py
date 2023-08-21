import unittest

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestKnight(unittest.TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty board": Case("d5", ['f4', 'f6', 'e3', 'e7',
                                       'c3', 'c7', 'b4', 'b6']),
            "target field occupied by own piece": Case("d5",
                                                       ['f6', 'e3',
                                                        'e7', 'c3', 'c7', 'b4',
                                                        'b6']).with_piece(
                Color.WHITE, "f4"),
            "target field occupied by enemy piece": Case("d5", [
                'f4', 'f6', 'e3', 'e7',
                'c3', 'c7', 'b4', 'b6']).with_piece(Color.BLACK, "f4"),
            "positioned in the corner": Case("h1", ['g3', 'f2']),
        }

        for name, test_case in test_cases.items():
            with self.subTest(name):
                knight = Piece(PieceType.KNIGHT, Color.WHITE)

                test_case.run(knight, self)

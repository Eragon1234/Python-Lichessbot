from unittest import TestCase

from game.piece import Piece
from game.piece.color import Color
from game.piece.piece_type import PieceType
from game.piece.tests.case import Case


class TestPawn(TestCase):
    def test_generate_possible_positions(self):
        test_cases: dict[str, Case] = {
            "empty board": Case("d5", ["d6"]),
            "field in front occupied by own piece": Case(
                "d5", []).with_piece(Color.WHITE, "d6"),
            "field in front occupied by enemy piece": Case(
                "d5", []).with_piece(Color.BLACK, "d6"),
            "field left front occupied by enemy piece": Case(
                "d5",
                ["e6", "d6"]).with_piece(Color.BLACK, "e6"),
            "field right front occupied by enemy piece": Case(
                "d5",
                ["c6", "d6"]).with_piece(Color.BLACK, "c6"),
            "field right front occupied by own piece": Case(
                "d5",
                ["d6"]).with_piece(Color.WHITE, "c6"),
            "field left front occupied by own piece": Case(
                "d5", ["d6"]).with_piece(Color.WHITE, "e6"),
            "possible enpassant": Case(
                "d5", ["d6", "e6"]
            ).with_piece(Color.BLACK, "e5").with_en_passant("e6"),
            "test promotion": Case(
                "d7", [
                    "d8q", "d8r", "d8b", "d8n"
                ]
            )
        }

        pawn = Piece(PieceType.PAWN, Color.WHITE)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = pawn.moves(test_case.board, test_case.position,
                                    test_case.en_passant)

                self.assertCountEqual(test_case.expected, actual)

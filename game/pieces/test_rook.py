from unittest import TestCase

from game import Rook
from game.types import Position, Positions


class TestRook(TestCase):
    def test_generate_possible_positions(self):
        class Case:
            def __init__(self, position: Position, expected: Positions):
                self.position = position
                self.expected = expected
                from game._chessboard import _ChessBoard
                self.board = _ChessBoard.from_fen("8/8/8/8/8/8/8/8 w - - 0 1").color_board()

            def with_piece(self, color: bool | str, x: int, y: int):
                self.board[x, y] = color
                return self

        test_cases: dict[str, Case] = {
            "completely empty board": Case((4, 4), [
                (4, 5), (4, 6), (4, 7), (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4),
                (0, 4)
            ]),
            "field in front occupied by own piece": Case((4, 4), [
                (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4), (0, 4)
            ]).with_piece(True, 4, 5),
            "field in front occupied by enemy piece": Case((4, 4), [
                (4, 3), (4, 2), (4, 1), (4, 0), (5, 4), (6, 4), (7, 4), (3, 4), (2, 4), (1, 4), (0, 4), (4, 5)
            ]).with_piece(False, 4, 5),
        }

        rook = Rook(True)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = rook.generate_possible_positions(test_case.position, test_case.board)

                self.assertCountEqual(test_case.expected, actual)
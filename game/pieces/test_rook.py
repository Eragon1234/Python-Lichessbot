from unittest import TestCase

from game import Rook


class TestRook(TestCase):
    def test_generate_possible_positions(self):
        class Case:
            def __init__(self, position: tuple[int, int], expected: list[tuple[int, int]]):
                self.position = position
                self.expected = expected
                self.board: list[list[str | bool]] = [["EmptyField" for _ in range(8)] for _ in range(8)]

            def with_piece(self, color: bool | str, x: int, y: int):
                self.board[y][x] = color
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
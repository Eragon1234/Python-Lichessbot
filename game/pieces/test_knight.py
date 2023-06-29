import unittest

from game.pieces.knight import Knight


class TestKnight(unittest.TestCase):
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
            "empty board": Case((4, 4), [
                (2, 3),
                (2, 5),
                (3, 2),
                (3, 6),
                (5, 2),
                (5, 6),
                (6, 3),
                (6, 5)
            ]),
            "target field occupied by own piece": Case((4, 4), [
                (2, 5),
                (3, 2),
                (3, 6),
                (5, 2),
                (5, 6),
                (6, 3),
                (6, 5)
            ]).with_piece(True, 2, 3),
            "target field occupied by enemy piece": Case((4, 4), [
                (2, 3),
                (2, 5),
                (3, 2),
                (3, 6),
                (5, 2),
                (5, 6),
                (6, 3),
                (6, 5)
            ]).with_piece(False, 2, 3),
            "positioned in the corner": Case((0, 0), [
                (1, 2),
                (2, 1)
            ]),
        }

        knight = Knight(True)
        for name, test_case in test_cases.items():
            with self.subTest(name):
                actual = knight.generate_possible_positions(test_case.position, test_case.board)

                self.assertCountEqual(test_case.expected, actual)
from typing import List, Tuple
from unittest import TestCase

from game import King


class TestKing(TestCase):
    def test_generate_possible_positions(self):
        class Case:
            def __init__(self, position: (int, int), message: str, expected: List[Tuple[int, int]]):
                self.position = position
                self.message = message
                self.expected = expected
                self.board: List[List[str | bool]] = [["EmptyField" for _ in range(8)] for _ in range(8)]

            def with_piece(self, color: bool, x: int, y: int):
                self.board[y][x] = color
                return self

        test_cases: List[Case] = [
            Case((0, 0), "King shouldn't move out of the board", [
                (1, 0),
                (0, 1), (1, 1)
            ]),
            Case((4, 4), "King should move to all adjacent positions", [
                (3, 3), (4, 3), (5, 3),
                (3, 4), (5, 4),
                (3, 5), (4, 5), (5, 5)
            ]),
            Case((4, 4), "King shouldn't move to positions occupied by own pieces", [
                (3, 3), (4, 3), (5, 3),
                (5, 4),
                (3, 5), (4, 5), (5, 5)
            ]).with_piece(True, 3, 4),
            Case((4, 4), "King should move to positions occupied by enemy pieces", [
                (3, 3), (4, 3), (5, 3),
                (3, 4), (5, 4),
                (3, 5), (4, 5), (5, 5)
            ]).with_piece(False, 3, 4),
        ]

        king = King(True)
        for test_case in test_cases:
            actual = king.generate_possible_positions(test_case.position, test_case.board)

            self.assertCountEqual(test_case.expected, actual, test_case.message)

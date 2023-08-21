import unittest

from game.coordinate import Coordinate
from game.piece.color import Color
from game.piece.piece import Piece
from game.piece.piece_type import PieceType


class Case:
    def __init__(self, pos: str, expected: list[str]):
        self.position = Coordinate.from_uci(pos)
        self.expected = [pos + target for target in expected]

        from game.board import Board
        self.board = Board.from_fen("8/8/8/8/8/8/8/8 w - - 0 1")
        self.en_passant = None

    def with_piece(self, color: Color, pos: str):
        x, y = Coordinate.from_uci(pos)
        self.board[x, y] = Piece(PieceType.PAWN, color)
        return self

    def with_en_passant(self, pos: str):
        self.en_passant = Coordinate.from_uci(pos)
        return self

    def run(self, piece: Piece, t: unittest.TestCase):
        actual = piece.moves(self.board, self.position, self.en_passant)

        t.assertCountEqual(self.expected, [move.uci() for move in actual])

import unittest

from game import ChessBoard
from game.piece.color import Color


class TestUnmove(unittest.TestCase):
    moveDepth = 3

    def test_unmove(self):
        test_fens = [
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        ]
        for fen in test_fens:
            with self.subTest(fen=fen):
                board = ChessBoard(fen)
                self.move_and_unmove(board, Color.WHITE, self.moveDepth)

    def move_and_unmove(self, board: ChessBoard, color: Color, depth: int):
        if depth == 0:
            return
        board_state = board.fen()
        for move in board.legal_moves():
            board.move(move)
            self.move_and_unmove(board, color.enemy(), depth - 1)
            board.unmove()
            self.assertEqual(board.fen(), board_state,
                             f'board state changed after unmove: {move.uci()}')

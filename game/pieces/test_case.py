from game import Piece
from game.pieces import Color, PieceType
from game.types import Position


class Case:
    def __init__(self, position: Position, expected: list[Position]):
        self.position = position
        self.expected = expected
        from game._chessboard import _ChessBoard
        self.board = _ChessBoard.from_fen("8/8/8/8/8/8/8/8 w - - 0 1")

    def with_piece(self, color: Color, x: int, y: int):
        self.board[x, y] = Piece(PieceType.PAWN, color)
        return self

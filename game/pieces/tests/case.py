from game import Piece
from game.pieces import Color, PieceType
from game.coordinate import Coordinate


class Case:
    def __init__(self, position: Coordinate, expected: list[Coordinate]):
        self.position = position
        self.expected = expected
        from game._chessboard import _ChessBoard
        self.board = _ChessBoard.from_fen("8/8/8/8/8/8/8/8 w - - 0 1")
        self.en_passant = None

    def with_piece(self, color: Color, x: int, y: int):
        self.board[x, y] = Piece(PieceType.PAWN, color)
        return self

    def with_en_passant(self, x: int, y: int):
        self.en_passant = (x, y)
        return self

from game.coordinate import Coordinate
from game.move.uci import move_from_uci
from game.piece.color import Color
from game.piece.piece import Piece
from game.piece.piece_type import PieceType


class Case:
    def __init__(self, pos: str, expected: list[str]):
        self.position = Coordinate.from_uci(pos)
        self.expected = [move_from_uci(pos + e) for e in expected]

        from game._chessboard import _ChessBoard
        self.board = _ChessBoard.from_fen("8/8/8/8/8/8/8/8 w - - 0 1")
        self.en_passant = None

    def with_piece(self, color: Color, pos: str):
        x, y = Coordinate.from_uci(pos)
        self.board[x, y] = Piece(PieceType.PAWN, color)
        return self

    def with_en_passant(self, pos: str):
        self.en_passant = Coordinate.from_uci(pos)
        return self

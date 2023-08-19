from game.coordinate import Coordinate
from game.move._chessboard import _ChessBoard
from game.move.move import Move
from game.piece.color import Color
from game.piece.piece_type import PieceType


class NormalMove(Move):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

        self.old_en_passant = "-"
        self.old_halfmove_clock = 0

    def uci(self) -> str:
        return f"{self.start_field.uci()}{self.target_field.uci()}"

    @classmethod
    def from_uci(cls, uci: str) -> "NormalMove":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        return cls(start_field, target_field)

    def move(self, board: _ChessBoard):
        self.old_en_passant = board.en_passant

        super().move(board)

        board.turn = board.turn.enemy()

        board.en_passant = "-"

        self.old_halfmove_clock = board.halfmove_clock

        if self.captured_piece.type is not PieceType.EMPTY:
            board.halfmove_clock = -1

        board.halfmove_clock += 1

        if board.turn is Color.WHITE:
            board.fullmove_number += 1

    def undo(self, board: _ChessBoard):
        board.en_passant = self.old_en_passant

        super().undo(board)

        board.turn = board.turn.enemy()

        board.halfmove_clock = self.old_halfmove_clock

        if board.turn is Color.BLACK:
            board.fullmove_number -= 1

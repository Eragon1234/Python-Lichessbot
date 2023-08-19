from game.coordinate import Coordinate
from game.move._chessboard import _ChessBoard
from game.move.move import Move


class NormalMove(Move):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

        self.old_en_passant = "-"

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

    def undo(self, board: _ChessBoard):
        board.en_passant = self.old_en_passant

        super().undo(board)

        board.turn = board.turn.enemy()

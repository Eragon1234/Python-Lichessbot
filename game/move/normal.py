from game.coordinate import Coordinate
from game.move.board import Board
from game.move.move import Move
from game.piece.color import Color
from game.piece.piece_type import PieceType


class NormalMove(Move):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

    def uci(self) -> str:
        return f"{self.start_field.uci()}{self.target_field.uci()}"

    @classmethod
    def from_uci(cls, uci: str) -> "NormalMove":
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        return cls(start_field, target_field)

    def move(self, board: Board):
        super().move(board)

        board.turn = board.turn.enemy()

        board.en_passant = None

        if self.captured_piece.type is not PieceType.EMPTY:
            board.halfmove_clock = -1

        board.halfmove_clock += 1

        if board.turn is Color.WHITE:
            board.fullmove_number += 1

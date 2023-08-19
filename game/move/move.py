from abc import ABC, abstractmethod

from game.coordinate import Coordinate
from game.move._chessboard import _ChessBoard


class Move(ABC):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        self.start_field = start_field
        self.target_field = target_field

        self.captured_piece = None

    @abstractmethod
    def uci(self) -> str:
        return f"{self.start_field.uci()}{self.target_field.uci()}"

    @classmethod
    @abstractmethod
    def from_uci(cls, uci: str) -> "Move":
        pass

    @abstractmethod
    def move(self, board: _ChessBoard) -> None:
        self.captured_piece = board.do_move(self.start_field, self.target_field)

    @abstractmethod
    def undo(self, board: _ChessBoard) -> None:
        board.do_move(self.target_field, self.start_field)
        board[self.target_field] = self.captured_piece


class PureMove(Move):
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

    def uci(self) -> str:
        return super().uci()

    @classmethod
    def from_uci(cls, uci: str) -> "PureMove":
        raise NotImplementedError("PureMove cannot be created from uci")

    def move(self, board: _ChessBoard) -> None:
        super().move(board)

    def undo(self, board: _ChessBoard) -> None:
        super().undo(board)

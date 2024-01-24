from abc import ABC, abstractmethod

from game.coordinate import Coordinate
from game.move.board import Board


class Move(ABC):
    """
    Class representing a move in a game.
    It provides the functionality to execute and undo the move on a board.
    """
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        self.start_field = start_field
        self.target_field = target_field

        self.captured_piece = None

    @abstractmethod
    def uci(self) -> str:
        """Returns the uci representation of the move."""
        return f"{self.start_field.uci()}{self.target_field.uci()}"

    @classmethod
    @abstractmethod
    def from_uci(cls, uci: str) -> "Move":
        """Creates a move from the uci representation."""

    @abstractmethod
    def move(self, board: Board) -> None:
        """Executes the move on the board."""
        self.captured_piece = board.do_move(self.start_field, self.target_field)


class PureMove(Move):
    """
    Pure Move just moves a piece from one field to another.
    It does not capture any pieces, etc.
    """
    def __init__(self, start_field: Coordinate, target_field: Coordinate):
        super().__init__(start_field, target_field)

    def uci(self) -> str:
        return super().uci()

    @classmethod
    def from_uci(cls, uci: str) -> "PureMove":
        raise NotImplementedError("PureMove cannot be created from uci")

    def move(self, board: Board) -> None:
        super().move(board)

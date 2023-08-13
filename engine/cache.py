from typing import Protocol, Optional

from game import ChessBoard
from game.move import Move
from game.piece import Color

MoveEvaluation = tuple[Move, float]


class Cache(Protocol):
    def get(self, color: Color, board: ChessBoard, min_depth: int,
            default: Optional[MoveEvaluation] = None) -> Optional[MoveEvaluation]:
        """
        Gets the cached value for the given color and board if there is an
        evaluation with a depth that's greater than or equal to min_depth.

        If there isn't one, it returns default.
        """

    def put(self, color: Color, board: ChessBoard,
            depth: int, value: MoveEvaluation):
        """
        Puts the given value in the cache for the given color and board
        with the given depth.
        """


class NoCache(Cache):
    def get(self, color: Color, board: ChessBoard, min_depth: int,
            default: Optional[MoveEvaluation] = None) -> Optional[MoveEvaluation]:
        """Returns the default value."""
        return default

    def put(self, color: Color, board: ChessBoard,
            depth: int, value: MoveEvaluation):
        """Does nothing."""

from typing import Protocol, Optional

from game import ChessBoard
from game.move import Move
from game.piece import Color

MoveEvaluation = tuple[Move, float]


class Cache(Protocol):
    def get(self, color: Color, board: ChessBoard, min_depth: int,
            default: Optional[MoveEvaluation] = None) -> Optional[MoveEvaluation]:
        ...

    def put(self, color: Color, board: ChessBoard,
            depth: int, value: MoveEvaluation):
        ...


class NoCache(Cache):
    def get(self, color: Color, board: ChessBoard, min_depth: int,
            default: Optional[MoveEvaluation] = None) -> Optional[MoveEvaluation]:
        return default

    def put(self, color: Color, board: ChessBoard,
            depth: int, value: MoveEvaluation):
        pass

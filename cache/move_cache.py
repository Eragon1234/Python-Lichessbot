from typing import Optional

from cache.lru.cache import LRUCache
from engine.cache import MoveEvaluation
from game import ChessBoard
from game.piece import Color


class MoveCache:
    def __init__(self, size: int):
        self.cache: dict[Color, LRUCache[str, list[MoveEvaluation]]] = {
            Color.WHITE: LRUCache(size),
            Color.BLACK: LRUCache(size)
        }

    def get(self, color: Color, board: ChessBoard, min_depth: int,
            default: Optional[MoveEvaluation] = None) -> Optional[MoveEvaluation]:
        evaluations = self.cache[color].get(board.fen())
        if evaluations is None:
            return default

        if len(evaluations) < min_depth:
            return default

        return evaluations[-1]

    def set(self, color: Color, board: ChessBoard,
            depth: int, value: MoveEvaluation) -> None:
        evaluations = self.cache[color].get(board.fen())
        if evaluations is None:
            evaluations = []

        if depth > len(evaluations):
            evaluations.extend([None] * (depth - len(evaluations)))

        evaluations[depth - 1] = value

        self.cache[color].set(board.fen(), evaluations)

import logging
import time
from functools import cache
from itertools import count
from typing import Optional

from game import ChessBoard
from game.move import Move
from game.piece.color import Color
from playercolor import PlayerColor

MoveEvaluation = tuple[Optional[Move], float]


class Engine:
    """Class to generate the best possible moves, etc."""

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = ChessBoard(fen)

    def __hash__(self):
        return hash(self.board)

    def __eq__(self, other):
        return self.board == other.board

    def get_best_move(self, color: PlayerColor,
                      moves: list[str], seconds: int = 3) -> MoveEvaluation:
        """
        Returns the best possible move for the given color.

        Args:
            color (PlayerColor): the color for whom to generate the best moves
            moves (list[str]): moves since the start position
            seconds (int): the time to calculate the best move.

        Returns:
            tuple[str, int]: the move and the evaluation
        """
        exit_time = time.time() + seconds

        best_move = None
        value = -9999

        for depth in count(1):
            logging.info("Depth: %s", depth)
            best_move, value = self.calculate_best_move(color, depth)
            depth += 1
            if time.time() > exit_time:
                break

        return best_move, value

    def calculate_best_move(self, color: PlayerColor, depth: int) -> MoveEvaluation:
        color = Color.WHITE if color is PlayerColor.White else Color.BLACK

        return self.negamax(depth, -9999, 9999, color)

    @cache
    def negamax(self, depth: int, alpha: float, beta: float,
                color: Color) -> MoveEvaluation:
        if depth == 0:
            return None, self.material_difference(color)

        moves = list(self.board.legal_moves(color))
        moves = self.order_moves(moves)

        best_move = None
        max_value = -9999

        for move in moves:
            with self.board.test_move(move):
                _, value = self.negamax(depth - 1, -beta, -alpha, color.enemy())
                value = -value

                if value > max_value:
                    max_value = value
                    best_move = move

                alpha = max(alpha, max_value)

                if alpha >= beta:
                    break

        if best_move is None:
            max_value = -9999 if self.board.king_in_check(color) else 0

        return best_move, max_value

    def order_moves(self, moves: list[Move]) -> list[Move]:
        def sort_key(move: Move) -> int:
            return self.board.value_at(move.target_field)

        return sorted(moves, key=sort_key, reverse=True)

    def material_difference(self, color: Color) -> int:
        material_difference = self.board.material_difference()
        if color is Color.BLACK:
            material_difference = -material_difference

        return material_difference

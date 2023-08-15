import logging
import time
from itertools import count

from engine.cache import Cache, NoCache, MoveEvaluation
from game import ChessBoard
from game.move import Move
from game.piece import Color
from playercolor import PlayerColor

NULL_MOVE = Move.from_uci("d1e8")


class Engine:
    """Class to generate the best possible moves, etc."""

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
                 cache: Cache = None):
        self.board = ChessBoard(fen)

        self.cache = cache
        if self.cache is None:
            self.cache = NoCache()

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

        best_move = NULL_MOVE
        value = -9999

        for depth in count(1):
            logging.info(f"Depth: {depth}")
            best_move, value = self.calculate_best_move(color, depth)
            depth += 1
            if time.time() > exit_time:
                break

        return best_move, value

    def calculate_best_move(self, color: PlayerColor, depth: int) -> MoveEvaluation:
        color = Color.WHITE if color is PlayerColor.White else Color.BLACK

        return self.negamax(depth, -9999, 9999, color)

    def negamax(self, depth: int, alpha: float, beta: float,
                color: Color) -> MoveEvaluation:
        cached = self.cache.get(color, self.board, depth)
        if cached is not None:
            return cached

        if depth == 0:
            return NULL_MOVE, self.material_difference(color)

        moves = list(self.board.legal_moves(color))
        moves = self.order_moves(moves)

        best_move = None
        max_value = alpha

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

        self.cache.set(color, self.board, depth, (best_move, max_value))

        return best_move, max_value

    def order_moves(self, moves: list[Move]) -> list[Move]:
        def sort_key(move: Move) -> int:
            return self.board.board[move.target_field].value

        return sorted(moves, key=sort_key, reverse=True)

    def material_difference(self, color: Color) -> int:
        material_difference = self.board.material_difference()
        if color is Color.BLACK:
            material_difference = -material_difference

        return material_difference

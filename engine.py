from collections import defaultdict
from functools import partial

from game import ChessBoard
from game.move import Move
from game.piece import Color
from growing_list import GrowingList
from playercolor import PlayerColor

CacheState = tuple[ChessBoard, Color]

MoveEvaluation = tuple[Move, float]

Cache = dict[CacheState, GrowingList[MoveEvaluation]]

NULL_MOVE = Move.from_uci("d1e8")

MoveEvaluationGrowingList = partial(GrowingList, (None, -9999))


class Engine:
    """Class to generate the best possible moves, etc."""

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = ChessBoard(fen)

        self.cached_moves: Cache = defaultdict(MoveEvaluationGrowingList)

    def get_best_move(self, color: PlayerColor, moves: list[str]) -> MoveEvaluation:
        """
        Returns the best possible move for the given color.

        Args:
            color (PlayerColor): the color for whom to generate the best moves
            moves (list[str]): moves since the start position

        Returns:
            tuple[str, int]: the move and the evaluation
        """
        return self.calculate_best_move(color, 1)

    def calculate_best_move(self, color: PlayerColor, depth: int) -> MoveEvaluation:
        color = Color.WHITE if color is PlayerColor.White else Color.BLACK

        return self.negamax(depth, float("-inf"), float("inf"), color)

    def negamax(self, depth: int, alpha: float, beta: float,
                color: Color) -> MoveEvaluation:
        if (self.board, color) in self.cached_moves:
            if len(self.cached_moves[self.board, color]) > depth:
                return self.cached_moves[self.board, color][-1]

        if depth == 0:
            return NULL_MOVE, self.board.material_difference()

        moves = list(self.board.legal_moves(color))
        moves = self.order_moves(moves)

        best_move, max_value = self.cached_moves[self.board, color][-1]
        alpha = max(alpha, max_value)

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
            return NULL_MOVE, -9999

        self.cached_moves[self.board, color][depth] = best_move, max_value

        return best_move, max_value

    def order_moves(self, moves: list[Move]) -> list[Move]:
        def sort_key(move: Move) -> int:
            return self.board.board[move.target_field].value

        return sorted(moves, key=sort_key, reverse=True)

from game import ChessBoard
from game.move import Move
from game.piece import Color
from playercolor import PlayerColor

CacheState = tuple[ChessBoard, Color, int]

MoveEvaluation = tuple[Move, float]

NULL_MOVE = Move.from_uci("d1e8")


class Engine:
    """Class to generate the best possible moves, etc."""

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = ChessBoard(fen)

        self.cached_moves: dict[CacheState, MoveEvaluation] = {}

    def get_best_move(self, color: PlayerColor, moves: list[str]) -> MoveEvaluation:
        """
        Returns the best possible move for the given color.

        Args:
            color (PlayerColor): the color for whom to generate the best moves
            moves (list[str]): moves since the start position

        Returns:
            tuple[str, int]: the move and the evaluation
        """
        return self.calculate_best_move(color, 3)

    def calculate_best_move(self, color: PlayerColor, depth: int) -> MoveEvaluation:
        color = Color.WHITE if color == PlayerColor.White else Color.BLACK

        return self.negamax(depth, float("-inf"), float("inf"), color)

    def negamax(self, depth: int, alpha: float, beta: float,
                color: Color) -> MoveEvaluation:
        if (self.board, color, depth) in self.cached_moves:
            return self.cached_moves[self.board, color, depth]

        if depth == 0:
            return NULL_MOVE, self.board.material_difference()

        moves = self.board.legal_moves(color)

        best_move = None
        max_value = float("-inf")

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

        self.cached_moves[self.board, color, depth] = best_move, max_value

        return best_move, max_value

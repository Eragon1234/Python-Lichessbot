import logging

from game import ChessBoard


class Engine:
    """Class to generate the best possible moves, etc."""

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = ChessBoard(fen)

        self.cached_moves: dict[tuple[ChessBoard, bool, int], tuple[str, float]] = {}

    def get_best_move(self, color: str, moves: list[str]) -> tuple[str, float]:
        """ Returns the best possible move for the given color.

        Args:
            color (str): the color for whom to generate the best moves
            moves (list[str]): moves since the start position

        Returns:
            str: the best possible move
        """
        for_white = color == 'white'

        return self.calculate_best_move(for_white, 3)

    def opponents_move(self, move) -> None:
        logging.info("opponents turn")
        logging.info("opponent moved: %s", move)
        self.board.move(move)
        logging.info("opponent moved\n")

    def calculate_best_move(self, for_white: bool, depth: int) -> tuple[str, float]:
        if for_white:
            move = self.max(depth, float("-inf"), float("inf"))
        else:
            move = self.min(depth, float("-inf"), float("inf"))

        return move

    def max(self, depth: int, alpha: float, beta: float) -> tuple[str, float]:
        if (self.board, True, depth) in self.cached_moves:
            return self.cached_moves[self.board, True, depth]

        if depth == 0:
            return "", self.board.material_difference()

        moves = self.board.generate_possible_moves(True)

        max_value = alpha
        max_move = None

        for move in moves:
            with self.board.test_move(move):
                _, evaluation = self.min(depth - 1, max_value, beta)
                if evaluation > max_value:
                    max_value = evaluation
                    max_move = move
                    if max_value >= beta:
                        break

        if max_move is None:
            return "", -9999

        self.cached_moves[self.board, True, depth] = max_move, max_value

        return max_move, max_value

    def min(self, depth: int, alpha: float, beta: float) -> tuple[str, float]:
        if (self.board, False, depth) in self.cached_moves:
            return self.cached_moves[self.board, False, depth]

        if depth == 0:
            return "", self.board.material_difference()

        moves = self.board.generate_possible_moves(False)

        min_value = beta
        min_move = None

        for move in moves:
            with self.board.test_move(move):
                _, evaluation = self.max(depth - 1, alpha, min_value)
                if evaluation < min_value:
                    min_value = evaluation
                    min_move = move
                    if min_value <= alpha:
                        break

        if min_move is None:
            return "", 9999

        self.cached_moves[self.board, False, depth] = min_move, min_value

        return min_move, min_value

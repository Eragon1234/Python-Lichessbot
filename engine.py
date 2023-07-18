import logging
import sys
import typing

from game import ChessBoard


class Engine:
    """Class to generate the best possible moves, etc."""

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = ChessBoard(fen)
        self.positions = None

    def get_best_move(self, color: str, moves: list[str]) -> str:
        """ Returns the best possible move for the given color.

        Args:
            color (str): the color for whom to generate the best moves
            moves (list[str]): moves since the start position

        Returns:
            str: the best possible move
        """
        logging.info("my_move")

        for_white = color == 'white'

        best_move = self.calculate_best_move(for_white, 4)
        if isinstance(best_move, tuple):
            logging.info("Evaluation: %s", best_move[1])
            best_move = best_move[0]
        if isinstance(best_move, int):
            logging.fatal("best_move is int: %s", best_move)
            sys.exit(1)
        logging.info(best_move)
        self.board.move(best_move)
        return best_move

    def opponents_move(self, move) -> None:
        logging.info("opponents turn")
        logging.info("opponent moved: %s", move)
        self.board.move(move)
        logging.info("opponent moved\n")

    def calculate_best_move(self, for_white: bool, depth: int,
                            board: ChessBoard = None) -> str:
        if board is None:
            board = self.board

        if for_white:
            move = self.max(depth, float("-inf"), float("inf"), board, {}, True)
        else:
            move = self.min(depth, float("-inf"), float("inf"), board, {}, True)

        return move

    def max(self, depth: int, alpha: float, beta: float, board: ChessBoard,
            positions: dict[str, float] = None, return_move: bool = False) -> float | tuple[str, float]:
        if positions is None:
            positions = {}
        self.positions = positions
        moves = board.generate_possible_moves(True)
        moves.sort(key=self.get_sort_value_for_move)

        if len(moves) == 0:
            return -9999

        if depth == 0:
            return self.get_material_difference_for_move(moves[0])

        max_value = alpha
        max_move = moves[0]

        for move in moves:
            with board.test_move(move) as test_board:
                short_board = test_board.board.flat_short_board()

                if short_board in positions and not return_move:
                    return positions.get(short_board)

                evaluation = self.min(depth - 1, max_value, beta, test_board, positions)
                evaluation = int(evaluation)
                if evaluation > max_value:
                    max_value = evaluation
                    max_move = move
                    if max_value >= beta:
                        break

                positions[short_board] = max_value
        if return_move:
            return max_move, max_value
        return max_value

    def min(self, depth: int, alpha: float, beta: float, board: ChessBoard,
            positions: dict[str, float] = None, return_move: bool = False) -> float | tuple[str, float]:
        if positions is None:
            positions = {}
        self.positions = positions
        moves = board.generate_possible_moves(False)

        if len(moves) == 0:
            return 9999

        if depth == 0:
            return self.get_material_difference_for_move(moves[0])

        min_value = beta
        min_move = moves[0]

        for move in moves:
            with board.test_move(move) as test_board:
                short_board = test_board.board.flat_short_board()

                if short_board in positions and not return_move:
                    return positions.get(short_board)

                evaluation = self.max(depth - 1, alpha, min_value, test_board, positions)
                evaluation = int(evaluation)
                if evaluation < min_value:
                    min_value = evaluation
                    min_move = move
                    if min_value <= alpha:
                        break

                positions[short_board] = min_value
        if return_move:
            return min_move, min_value
        return min_value

    def get_material_difference_for_move(self, move: str, board: ChessBoard = None) -> int:
        if board is None:
            board = self.board
        with board.test_move(move) as test_board:
            evaluation = test_board.board.material_difference()
        return evaluation

    def get_sort_value_for_move(self, move: str) -> int:
        if self.positions is not None:
            with self.board.test_move(move) as board:
                short_board = board.board.flat_short_board()
                if short_board in self.positions:
                    return self.positions.get(short_board)
        return self.get_material_difference_for_move(move)

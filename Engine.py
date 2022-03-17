import numpy as np

from Game.Board import Board


class Engine:
    """
    Class to generate the best possible moves etc.
    """

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = Board(fen)
        self.positions = None

    def move(self, game_id, color, moves, move_fn):
        """ handles the calculations for the best possible moves

        Args:
            game_id (string): the id of the game to move in
            color (string): the color for whom to generate the best moves
            moves (string): moves since the start position
            move_fn (fn): function to make the move
        """
        for_white = color == 'white'

        best_move = self.calculate_best_move(for_white, 2)
        print("Evaluation:", best_move[1])
        move = best_move[0]
        print(move)
        self.board.move(move)
        move_fn(game_id, move)
        print("moved")

    def opponents_move(self, move):
        self.board.move(move)
        print("opponent moved")

    def calculate_best_move(self, for_white, depth, board=None):
        if board is None:
            board = self.board

        if for_white:
            move = self.max(depth, float("-inf"), float("inf"), board, {}, True)
        else:
            move = self.min(depth, float("-inf"), float("inf"), board, {}, True)

        return move

    def max(self, depth, alpha, beta, board, positions=None, return_move=False):
        if positions is None:
            positions = {}
        moves = board.generate_possible_moves(True)
        moves.sort(key=lambda move: self.get_sort_value_for_move(move))

        if len(moves) == 0:
            return float("-inf")

        if depth == 0:
            return self.get_value_difference_for_move(moves[0])

        max_value = alpha
        max_move = moves[0]

        for move in moves:
            board_key = self.board.test_move(move, board)
            short_board = tuple(np.array(self.board.testBoards[board_key].generate_short_board()).flat)

            if short_board in positions and not return_move:
                return positions.get(short_board)

            evaluation = self.min(depth - 1, max_value, beta, board.testBoards[board_key], positions)
            evaluation = int(evaluation)
            if evaluation > max_value:
                max_value = evaluation
                max_move = move
                if max_value >= beta:
                    break

            positions[short_board] = max_value
            self.board.pop_test_board(board_key)
        if return_move:
            self.positions = positions
            return max_move, max_value
        return max_value

    def min(self, depth, alpha, beta, board, positions=None, return_move=False):
        if positions is None:
            positions = {}
        moves = board.generate_possible_moves(False)

        if len(moves) == 0:
            return float("inf")

        if depth == 0:
            return self.get_value_difference_for_move(moves[0])

        min_value = beta
        min_move = moves[0]

        for move in moves:
            board_key = self.board.test_move(move, board)
            short_board = tuple(np.array(self.board.testBoards[board_key].generate_short_board()).flat)

            if short_board in positions and not return_move:
                return positions.get(short_board)

            evaluation = self.max(depth - 1, alpha, min_value, board.testBoards[board_key], positions)
            evaluation = int(evaluation)
            if evaluation < min_value:
                min_value = evaluation
                min_move = move
                if min_value <= alpha:
                    break

            positions[short_board] = min_value
            self.board.pop_test_board(board_key)
        if return_move:
            return min_move, min_value
        return min_value

    def get_value_difference_for_move(self, move, board=None):
        if board is None:
            board = self.board
        board = self.board.pop_test_board(self.board.test_move(move, board))
        evaluation = board.calculate_value_difference()
        return evaluation

    def get_material_difference_for_move(self, move, board=None):
        if board is None:
            board = self.board
        board = self.board.pop_test_board(self.board.test_move(move, board))
        evaluation = board.calculate_material_difference()
        return evaluation

    def get_sort_value_for_move(self, move):
        if self.positions is not None:
            board = self.board.pop_test_board(self.board.test_move(move))
            short_board = board.generate_short_board()
            if short_board in tuple(self.positions):
                return self.positions.get(short_board)
        return self.get_value_difference_for_move(move)

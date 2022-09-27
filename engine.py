from game import Board


# TODO: implement exceptions for checkmate and impossible moves
# TODO: implement re-moving of all moves to go on in a game after an error
# TODO: optimize and refactor saving of things
# TODO: implement depth depended caching
# TODO: optimize position evaluation and change bonus_map to multiplicator instead of bonus points


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
        print("my_move")
        for_white = color == 'white'

        best_move = self.calculate_best_move(for_white, 4)
        if isinstance(best_move, tuple):
            print("Evaluation:", best_move[1])
            best_move = best_move[0]
        print(best_move)
        self.board.move(best_move)
        move_fn(game_id, best_move)
        print("moved")
        print("-------------------------------------------------------------------------------------------")

    def opponents_move(self, move):
        print("opponents turn")
        print("opponent moved:", move)
        self.board.move(move)
        print("opponent moved")
        print("---------------------------------------------------------------------------------------")

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
        self.positions = positions
        moves = board.generate_possible_moves(True)
        moves.sort(key=lambda move: self.get_sort_value_for_move(move))

        if depth == 0:
            if len(moves) == 0:
                return -9999
            return self.get_value_difference_for_move(moves[0])

        if len(moves) == 0:
            return -9999

        max_value = alpha
        max_move = moves[0]

        for move in moves:
            with board.test_move(move) as test_board:
                short_board = test_board.generate_flat_short_board()

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

    def min(self, depth, alpha, beta, board, positions=None, return_move=False):
        if positions is None:
            positions = {}
        self.positions = positions
        moves = board.generate_possible_moves(False)

        if depth == 0:
            if len(moves) == 0:
                return 9999
            return self.get_value_difference_for_move(moves[0])

        if len(moves) == 0:
            return 9999

        min_value = beta
        min_move = moves[0]

        for move in moves:
            with board.test_move(move) as test_board:
                short_board = test_board.generate_flat_short_board()

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

    def get_value_difference_for_move(self, move, board=None):
        if board is None:
            board = self.board
        with board.test_move(move) as test_board:
            evaluation = test_board.calculate_value_difference()
        return evaluation

    def get_material_difference_for_move(self, move, board=None):
        if board is None:
            board = self.board
        with board.test_move(move) as test_board:
            evaluation = test_board.calculate_material_difference()
        return evaluation

    def get_sort_value_for_move(self, move):
        if self.positions is not None:
            with self.board.test_move(move) as board:
                short_board = board.generate_flat_short_board()
                if short_board in self.positions:
                    return self.positions.get(short_board)
        return self.get_value_difference_for_move(move)

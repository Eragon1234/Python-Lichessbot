import numpy as np

from Game.Board import Board


class Engine:
    """
    Class to generate the best possible moves etc.
    """

    def __init__(self, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.board = Board(fen)

    def move(self, gameId, color, moves, moveFn):
        """ handles the calculations for the best possible moves

        Args:
            gameId (string): the id of the game to move in
            color (string): the color for whom to generate the best moves
            moves (string): moves since the start position
            moveFn (fn): function to make the move
        """
        forWhite = color == 'white'
        
        bestMove = self.calculate_best_move(forWhite, 1)
        print("Evaluation:", bestMove[1])
        move = bestMove[0]
        print(move)
        self.board.move(move)
        moveFn(gameId, move)
        print("moved")

    def opponents_move(self, move):
        self.board.move(move)
        print("opponent moved")

    def calculate_best_move(self, forWhite, depth, board=False):
        if not board:
            board = self.board

        if forWhite:
            move = self.max(depth, float("-inf"), float("inf"), board, {}, True)
        else:
            move = self.min(depth, float("-inf"), float("inf"), board, {}, True)
        
        return move
    
    def max(self, depth, alpha, beta, board, positions={}, returnMove=False):
        moves = board.generate_possible_moves(True)

        if len(moves) == 0:
            return float("-inf")
            
        if depth == 0:
            return self.get_value_difference_for_move(moves[0])

        maxValue = alpha
        maxMove = moves[0]

        for move in moves:
            boardKey = self.board.test_move(move, board)
            shortBoard = tuple(np.array(self.board.testBoards[boardKey].generate_short_board()).flat)

            if shortBoard in positions and not returnMove:
                return positions.get(shortBoard)
            
            evaluation = self.min(depth - 1, maxValue, beta, board.testBoards[boardKey], positions)
            evaluation = int(evaluation)
            if evaluation > maxValue:
                maxValue = evaluation
                maxMove = move
                if maxValue >= beta:
                    break

            positions[shortBoard] = maxValue
            self.board.pop_test_board(boardKey)
        if returnMove:
            return maxMove, maxValue
        return maxValue

    def min(self, depth, alpha, beta, board, positions={}, returnMove=False):
        moves = board.generate_possible_moves(False)

        if len(moves) == 0:
            return float("inf")

        if depth == 0:
            return self.get_value_difference_for_move(moves[0])
        
        minValue = beta
        minMove = moves[0]

        for move in moves:
            boardKey = self.board.test_move(move, board)
            shortBoard = tuple(np.array(self.board.testBoards[boardKey].generate_short_board()).flat)

            if shortBoard in positions and not returnMove:
                return positions.get(shortBoard)

            evaluation = self.max(depth - 1, alpha, minValue, board.testBoards[boardKey], positions)
            evaluation = int(evaluation)
            if evaluation < minValue:
                minValue = evaluation
                minMove = move
                if minValue <= alpha:
                    break

            positions[shortBoard] = minValue
            self.board.pop_test_board(boardKey)
        if returnMove:
            return minMove, minValue
        return minValue

    def get_value_difference_for_move(self, move, board=False):
        if not board:
            board = self.board
        board = self.board.pop_test_board(self.board.test_move(move, board))
        evaluation = board.calculate_value_difference()
        return evaluation

    def get_material_difference_for_move(self, move, board=False):
        if not board:
            board = self.board
        board = self.board.pop_test_board(self.board.test_move(move, board))
        evaluation = board.calculate_material_difference()
        return evaluation
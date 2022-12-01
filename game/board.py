import random

import numpy as np
from numpy import ndarray

from .pieces import EmptyField, Pawn, Bishop, Knight, Rook, Queen, King
from .pieces.abstract_piece import AbstractPiece
from .test_move import TestMove


class Board:
    """
    a class to handle the current board state, making moves, generating possible Moves etc.
    """

    # an array for moved moves
    moves: [str] = []

    # a dictionary to save the possible moves
    possible_moves = {}
    # a dictionary for saving value differences
    value_differences = {}

    # the corresponding letter for the indexes of the columns
    columns = {
        '0': 'a',
        '1': 'b',
        '2': 'c',
        '3': 'd',
        '4': 'e',
        '5': 'f',
        '6': 'g',
        '7': 'h'
    }

    rows = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }

    # an array to keep track of the castle rights of black and white
    castle = {
        'white': {'king_side': False, 'queen_side': False},
        'black': {'king_side': False, 'queen_side': False}
    }

    captured_pieces = []

    en_passant_field = "-"

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        # loads the board with the given fen
        self.load_board_with_fen(fen)
        self.color_board = None
        self.short_board = None
        self.flat_short_board = None

    def move(self, move: str) -> None:
        """ makes a move on the board

        Args:
            move (UCIMove): the move to move
        """
        self.color_board = None
        self.short_board = None
        self.flat_short_board = None
        self.en_passant_field = "-"

        # appending the move to the array of moves
        self.moves.append(move)

        # converting the UCIMove into a coordinate move
        move = self.uci_into_coordinate_move(move)

        start_field_coordinates = (move[0][1], move[0][0])
        target_field_coordinates = (move[1][1], move[1][0])

        # getting the moving piece
        moving_piece = self.board[start_field_coordinates]
        # emptying the startField
        self.board[start_field_coordinates] = EmptyField.get_self()
        # setting the targetField to the moving_piece
        self.captured_pieces.append(self.board[move[1][1], move[1][0]])
        self.board[target_field_coordinates] = moving_piece

        if moving_piece.lower_short == "p" and abs(move[0][1] - move[1][1]) == 2:
            new_x = move[0][0]
            new_y = int(move[0][1] - ((move[0][1] - move[1][1]) / 2))
            self.en_passant_field = self.coordinate_moves_into_uci([((new_x, new_y), (0, 0))])[0][:2]

    def unmove(self, move: str) -> None:
        self.color_board = None
        self.short_board = None
        self.flat_short_board = None

        # removing the move to the array of moves
        self.moves.remove(move)
        # converting the UCIMove into a coordinate move
        move = self.uci_into_coordinate_move(move)

        start_field_coordinates = (move[1][1], move[1][0])
        target_field_coordinates = (move[0][1], move[0][0])
        # getting the moved piece
        moved_piece = self.board[start_field_coordinates]
        captured_piece = self.captured_pieces.pop()
        # adding the moved piece to the startField
        self.board[target_field_coordinates] = moved_piece
        self.board[start_field_coordinates] = captured_piece

    def test_move(self, move: str) -> TestMove:
        return TestMove(self, move)

    def generate_possible_moves(self, for_white: bool = True, return_pseudo_legal_moves: bool = False) -> list[str]:
        """ generating all possible moves in the current position

        Args:
            for_white (bool): for which color to generate the moves for. Defaults to True.
            return_pseudo_legal_moves(bool): if moves should be returned including pseudo-legal moves. Defaults to False

        Returns:
            list: a list of possible moves in UCIMove format
        """
        short_board = self.generate_flat_short_board()
        if short_board in self.possible_moves:
            return self.possible_moves.get(short_board)

        coordinate_moves = self.generate_possible_coordinate_moves(for_white)
        # converting coordinate moves into UCIMoves
        moves = self.coordinate_moves_into_uci(coordinate_moves)

        if return_pseudo_legal_moves:
            return moves

        evaluations = {}
        for move in tuple(moves):
            with self.test_move(move) as board:
                test_moves = board.generate_possible_moves(not for_white, True)
                max_evaluation = float("-inf")
                min_evaluation = float("inf")
                is_check = False
                for test_move in test_moves:
                    with self.test_move(test_move) as test_board:
                        evaluation = test_board.calculate_value_difference()
                        if evaluation > max_evaluation:
                            max_evaluation = evaluation

                        if evaluation < min_evaluation:
                            min_evaluation = evaluation

                        found_king = False
                        for piece in tuple(self.board.flat):
                            if piece.lower_short == "k" and piece.is_white == for_white:
                                found_king = True

                        if not found_king:
                            is_check = True

                if is_check:
                    moves.remove(move)
                    continue

                if for_white:
                    evaluations[move] = max_evaluation
                else:
                    evaluations[move] = min_evaluation

        if len(moves) == len(evaluations):
            moves.sort(key=lambda move: evaluations.get(move), reverse=for_white)

        self.possible_moves[short_board] = moves

        return moves

    def generate_possible_coordinate_moves(self, for_white: bool | str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """ generates the possible coordinate moves for the passed color

        Args:
            for_white: the color of the pieces to generate the possible moves from

        Returns:
            returns all possible coordinate moves for the passed color
        """
        coordinate_moves = []
        # generating the color_board as a parameter for the generate_possible_coordinate_moves method of the pieces
        color_board = self.generate_color_board()
        for piece in enumerate(tuple(self.board.flat)):
            # getting the coordinates of the piece in the flattened array
            coordinates = self.generate_coordinates_with_index(piece[0])
            piece = piece[1]

            # if piece is the color for which to generate moves for
            if piece.is_white == for_white:
                # generating possible positions
                new_positions = piece.generate_possible_positions(coordinates, color_board)
                # appending every position with the start and end coordinates
                for new_position in new_positions:
                    if len(str(new_position[1])) > 1:
                        new_position = new_position[0]
                    coordinate_moves.append((coordinates, new_position))
        return coordinate_moves

    def calculate_material_difference(self) -> int:
        """ calculates the material difference between white and black

        Returns:
            int: the material difference
        """

        material_difference = sum([piece.value for piece in tuple(self.board.flat) if piece.short != 'e'])
        return material_difference

    def calculate_value_difference(self) -> int:
        """ calculates the difference of the values of the pieces between white and black

        Returns:
            int: the material difference
        """
        short_board = self.generate_flat_short_board()
        if short_board in self.value_differences:
            return self.value_differences.get(short_board)

        material_difference = sum([piece.value for piece in tuple(self.board.flat)])
        self.value_differences[short_board] = material_difference
        return material_difference

    @staticmethod
    def generate_coordinates_with_index(index: int) -> tuple[int, int]:
        """ calculates the coordinates of a piece on the given index in 1d array with the length 64

        Args:
            index (int): the index in the 1d array

        Returns:
            tuple: the x and y coordinates of the piece
        """
        x = index % 8
        y = index // 8
        return x, y

    @staticmethod
    def generate_index_with_coordinates(coordinates: tuple[int, int]) -> int:
        x = coordinates[0]
        y = coordinates[1]
        index = (x + y * 8)
        return index

    def generate_color_board(self) -> list[list[bool | str]]:
        """ converts the current board state into a board with True, False and EmptyField standing for the colors

        Returns:
            list: a 2d array with values True for white, False for black and EmptyField for an empty field
        """
        if self.color_board is not None:
            return self.color_board
        color_board = []
        for row in self.board:
            color_board.append([])
            for piece in row:
                color_board[-1].append(piece.is_white)

        if self.en_passant_field != "-":
            en_passant_coordinate = self.uci_into_coordinate_move(f"{self.en_passant_field}h7")[:2][0]
            color_board[en_passant_coordinate[1]][en_passant_coordinate[0]] = "enemy"

        self.color_board = color_board
        return color_board

    def generate_short_board(self) -> list[list[str]]:
        """ converts the current board state into a board with the shorts of the pieces

        Returns:
            list: a 2d array with the shorts of the pieces instead of the objects
        """
        if self.short_board is not None:
            return self.short_board
        short_board = []
        for row in self.board:
            short_board.append([])
            for piece in row:
                short_board[-1].append(piece.short)

        self.short_board = short_board
        return short_board

    def generate_flat_short_board(self) -> tuple[str]:
        """ converts the current board state into a board with the shorts of the pieces

        Returns:
            tuple: a 1d tuple containing the shorts of the pieces
        """
        if self.flat_short_board is None:
            self.flat_short_board = tuple([piece.short for piece in self.board.flat])
        return self.flat_short_board

    def coordinate_moves_into_uci(self, coordinate_moves: tuple[tuple[int, int], tuple[int, int]]) -> list[str]:
        """ converts the passed array of coordinate moves into an array of UCIMoves

        Args:
            coordinate_moves (list): a list containing tuples with the startField and the targetField as x, y tuples

        Returns:
            list: a list of string which are moves in the UCI Notation
        """
        moves = []
        for coordinateMove in coordinate_moves:
            x1 = self.columns[
                f"{coordinateMove[0][0]}"]  # getting the letter for the column of the startField with the x number
            y1 = coordinateMove[0][1] + 1
            x2 = self.columns[
                f"{coordinateMove[1][0]}"]  # getting the letter for the column of the endField with the x number
            y2 = coordinateMove[1][1] + 1

            # combining these values to a string
            move = f"{x1}{y1}{x2}{y2}"
            moves.append(move)
        return moves

    def uci_into_coordinate_move(self, uci_move: str) -> tuple[tuple[int, int], tuple[int, int]]:
        """ converts the passed UCIMove into a coordinate move

        Args:
            uci_move (string): the UCIMove to convert into an UCIMove

        Returns:
            tuple: the coordinate move corresponding to the passed UCIMove
        """
        x1 = self.rows.get(uci_move[0])
        y1 = int(uci_move[1]) - 1
        x2 = self.rows.get(uci_move[2])
        y2 = int(uci_move[3]) - 1
        coordinate_move = ((x1, y1), (x2, y2))
        return coordinate_move

    def load_board_with_fen(self, fen: str) -> ndarray:
        """ loads the board with the passed fen

        Args:
            fen (string): the fen to load the board of the board object with
        """
        board = []

        fen = fen.split()

        position_fen_by_row = fen[0].split("/")

        for rowFen in position_fen_by_row:
            board.append([])
            for char in rowFen:
                # checking for black pieces with fen code
                if char == 'p':
                    board[-1].append(Pawn(False))
                elif char == 'b':
                    board[-1].append(Bishop(False))
                elif char == 'n':
                    board[-1].append(Knight(False))
                elif char == 'r':
                    board[-1].append(Rook(False))
                elif char == 'q':
                    board[-1].append(Queen(False))
                elif char == 'k':
                    board[-1].append(King(False))

                # checking for white pieces with fen code
                elif char == 'P':
                    board[-1].append(Pawn(True))
                elif char == 'B':
                    board[-1].append(Bishop(True))
                elif char == 'N':
                    board[-1].append(Knight(True))
                elif char == 'R':
                    board[-1].append(Rook(True))
                elif char == 'Q':
                    board[-1].append(Queen(True))
                elif char == 'K':
                    board[-1].append(King(True))

                # checking for numbers to move n pieces further
                elif char.isdigit():
                    for i in range(0, int(char)):
                        board[-1].append(EmptyField.get_self())

        if len(fen) == 6:
            # looking if it's white or blacks turn
            if fen[1] == 'w':
                self.whitesMove = True
            else:
                self.whitesMove = False

            # setting the castle rights of black and white
            for char in fen[2]:
                if char == 'K':
                    self.castle['white']['king_side'] = True
                elif char == 'Q':
                    self.castle['white']['queen_side'] = True
                elif char == 'k':
                    self.castle['black']['king_side'] = True
                elif char == 'q':
                    self.castle['black']['queen_side'] = True

            self.en_passant_field = fen[3]  # setting the en_passant_field with the corresponding value of the fen
            self.number_of_plies_for_50_move_rule = fen[
                4]  # setting the number of plies since the last queen move or take for the 50 move rule
            self.next_move_number = fen[5]  # setting the number of the next move

        # setting self.board to the board
        board.reverse()
        board = np.array(board)
        self.board = board
        return board

    def generate_fen_for_board(self) -> str:
        """ generates the fen for the current board

        Returns:
            string: the fen string for the current position on the board
        """
        fen = '/'.join([''.join([piece.short for piece in row]) for row in self.board])
        return fen

    @staticmethod
    def generate_random_string(length: int) -> str:
        """ generates a random string with the specified length

        Args:
            length (int): the length the random string should be

        Returns:
            string: a random string of the specified length
        """
        random_string = ''
        for i in range(length):
            random_integer = random.randint(0, 255)  # getting a random integer in the range 0 to 255
            random_string += chr(random_integer)  # converting the number into a char and appending if to the string
        return random_string

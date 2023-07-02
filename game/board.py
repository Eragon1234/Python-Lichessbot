import numpy as np
from numpy import ndarray

from game.pieces import EmptyField, Pawn, Bishop, Knight, Rook, Queen, King
from game.pieces.abstract_piece import AbstractPiece
from game.uci import uci_string_into_coordinate, coordinate_into_uci_string, uci_into_coordinate_move, \
    coordinate_move_into_uci


class Board:
    """a class to handle the current board state, making moves, generating possible moves, etc."""

    # a dictionary to save the possible moves
    possible_moves = {}
    # a dictionary for saving value differences
    value_differences = {}

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moves: list[str] = []
        self.castle_rights: set[str] = set()

        self.captured_pieces: list[AbstractPiece] = []
        self.en_passant_field = "-"

        # loads the board with the given fen
        self.load_board_with_fen(fen)
        self.color_board = None
        self.short_board = None
        self.flat_short_board = None

        self.en_passant_takes = []

    def move(self, move: str) -> None:
        """ makes a move on the board

        Args:
            move (UCIMove): the move to move
        """
        self.color_board = None
        self.short_board = None
        self.flat_short_board = None

        # appending the move to the array of moves
        self.moves.append(move)

        # converting the UCIMove into a coordinate move
        move = uci_into_coordinate_move(move)

        start_field_coordinates = move[0][1], move[0][0]
        target_field_coordinates = move[1][1], move[1][0]

        # getting the moving piece
        moving_piece = self.board[start_field_coordinates]
        # emptying the startField
        self.board[start_field_coordinates] = EmptyField.get_self()
        # setting the targetField to the moving_piece
        self.captured_pieces.append(self.board[move[1][1], move[1][0]])
        self.board[target_field_coordinates] = moving_piece

        en_passant_taken_piece = None
        if self.en_passant_field != "-" and moving_piece.lower_short == "p":
            took_en_passant = target_field_coordinates == uci_string_into_coordinate(self.en_passant_field)
            if took_en_passant:
                if self.whites_move():
                    en_passant_taken_piece = self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]]
                    self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]] = EmptyField.get_self()
                else:
                    en_passant_taken_piece = self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]]
                    self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]] = EmptyField.get_self()

        self.en_passant_takes.append(en_passant_taken_piece)
        self.en_passant_field = "-"

        if moving_piece.lower_short == "p" and abs(move[0][1] - move[1][1]) == 2:
            new_x = move[0][0]
            new_y = int(move[0][1] - ((move[0][1] - move[1][1]) / 2))
            self.en_passant_field = coordinate_into_uci_string((new_x, new_y))

    def unmove(self, move: str) -> None:
        """undoes a move on the board"""
        self.color_board = None
        self.short_board = None
        self.flat_short_board = None

        # removing the move to the array of moves
        self.moves.remove(move)
        # converting the UCIMove into a coordinate move
        move = uci_into_coordinate_move(move)

        start_field_coordinates = (move[1][1], move[1][0])
        target_field_coordinates = (move[0][1], move[0][0])

        # getting the moved piece
        moved_piece = self.board[start_field_coordinates]
        captured_piece = self.captured_pieces.pop()
        # adding the moved piece to the startField
        self.board[target_field_coordinates] = moved_piece
        self.board[start_field_coordinates] = captured_piece

        en_passant_taken_piece = self.en_passant_takes.pop()
        if en_passant_taken_piece is not None:
            if self.whites_move():
                self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]] = en_passant_taken_piece
            else:
                self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]] = en_passant_taken_piece

    def whites_move(self):
        return len(self.moves) % 2 == 0

    class TestMove:
        """a class to test a move with the context manager"""

        def __init__(self, board: "Board", move: str):
            self.board = board
            self.move = move

        def __enter__(self) -> "Board":
            self.board.move(self.move)
            return self.board

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.board.unmove(self.move)

    def test_move(self, move: str) -> TestMove:
        """returns an object that can be used to test a move with the context manager"""
        return self.TestMove(self, move)

    def generate_possible_moves(self, for_white: bool = True, return_pseudo_legal_moves: bool = False) -> list[str]:
        """ Generating all possible moves in the current position

        Args: for_white (bool): for which color to generate the moves for. Defaults to True.
        return_pseudo_legal_moves (bool): if moves should be returned, including pseudo-legal moves. Defaults to False

        Returns:
            list: a list of possible moves in UCIMove format
        """
        short_board = self.generate_flat_short_board()
        if short_board in self.possible_moves:
            return self.possible_moves.get(short_board)

        coordinate_moves = self.generate_possible_coordinate_moves(for_white)
        # converting coordinate moves into UCIMoves
        moves = [coordinate_move_into_uci(move) for move in coordinate_moves]

        if return_pseudo_legal_moves:
            return moves

        remove_moves = []

        for move in moves:
            with self.test_move(move) as board:
                coordinate_moves = board.generate_possible_coordinate_moves(not for_white)
                is_check = False
                for coordinate_move in coordinate_moves:
                    x, y = coordinate_move[1]
                    attacked_field: AbstractPiece = board.board[y, x]

                    if attacked_field.lower_short == "k" and attacked_field.is_white == for_white:
                        is_check = True
                        break

                if is_check:
                    remove_moves.append(move)

        for move in remove_moves:
            moves.remove(move)

        self.possible_moves[short_board] = moves

        return moves

    def generate_possible_coordinate_moves(self, for_white: bool | str) -> list[
        tuple[tuple[int, int], tuple[int, int]]]:
        """ generates the possible coordinate moves for the passed color

        Args:
            for_white: the color of the pieces to generate the possible moves from

        Returns:
            returns all possible coordinate moves for the passed color
        """
        coordinate_moves = []
        # generating the color_board as a parameter for the generate_possible_coordinate_moves method of the pieces
        color_board = self.generate_color_board()
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                # getting the coordinates of the piece in the flattened array
                coordinates = (x, y)

                # if the piece is the color for which to generate moves for
                if piece.is_white == for_white:
                    # generating possible positions
                    new_positions = [(coordinates, new_position)
                                     for new_position in piece.generate_possible_positions(coordinates, color_board)]
                    # append the new positions to the coordinate_moves
                    coordinate_moves.extend(new_positions)
        return coordinate_moves

    def calculate_material_difference(self) -> int:
        """ calculates the material difference between white and black

        Returns:
            int: the material difference
        """
        material_difference = sum(piece.value for piece in tuple(self.board.flat) if piece.short != 'e')
        return material_difference

    def calculate_value_difference(self) -> int:
        """ calculates the difference of the values for the pieces between white and black

        Returns:
            int: the material difference
        """
        short_board = self.generate_flat_short_board()
        if short_board in self.value_differences:
            return self.value_differences.get(short_board)

        material_difference = sum(piece.value for piece in tuple(self.board.flat))
        self.value_differences[short_board] = material_difference
        return material_difference

    def generate_color_board(self) -> list[list[bool | str]]:
        """ converts the current board state into a board with True, False and EmptyField standing for the colors

        Returns:
            list: a 2d array with values True for white, False for black and EmptyField for an empty field
        """
        if self.color_board is not None:
            return self.color_board

        # create a 2d array with the colors of the pieces
        color_board = [[piece.is_white for piece in row] for row in self.board]

        if self.en_passant_field != "-":
            en_passant_coordinate = uci_into_coordinate_move(f"{self.en_passant_field}h7")[:2][0]
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
            self.flat_short_board = tuple(piece.short for piece in self.board.flat)
        return self.flat_short_board

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
                white = not char.islower()
                char = char.lower()
                if char == 'p':
                    board[-1].append(Pawn(white))
                elif char == 'b':
                    board[-1].append(Bishop(white))
                elif char == 'n':
                    board[-1].append(Knight(white))
                elif char == 'r':
                    board[-1].append(Rook(white))
                elif char == 'q':
                    board[-1].append(Queen(white))
                elif char == 'k':
                    board[-1].append(King(white))

                # checking for numbers to move n pieces further
                elif char.isdigit():
                    for _ in range(int(char)):
                        board[-1].append(EmptyField.get_self())

        if len(fen) == 6:
            # looking if it's white or blacks turn
            self.whitesMove = fen[1] == 'w'

            # setting the castle rights of black and white
            for char in fen[2]:
                self.castle_rights.add(char)

            self.en_passant_field = fen[3]  # setting the en_passant_field with the corresponding value of the fen
            self.number_of_plies_for_50_move_rule = fen[4]  # setting the current num of plies for 50 move rule
            self.next_move_number = fen[5]  # setting the number of the next move

        # setting self.board to the board
        board.reverse()
        board = np.array(board)
        self.board: ndarray[ndarray[AbstractPiece]] = board
        return board

    def generate_fen_for_board(self) -> str:
        """ generates the fen for the current board

        Returns:
            string: the fen string for the current position on the board
        """
        fen = '/'.join([''.join([piece.short for piece in row]) for row in self.board])
        return fen

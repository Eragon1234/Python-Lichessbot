from game._board import position_to_coordinate
from game._chessboard import _ChessBoard
from game.pieces import EmptyField
from game.pieces.abstract_piece import AbstractPiece
from game.types import Move
from game.uci import uci_string_into_coordinate, coordinate_into_uci_string, \
    uci_into_coordinate_move, coordinate_move_into_uci


class ChessBoard:
    """a class to handle the current board state, making moves, generating possible moves, etc."""

    # a dictionary to save the possible moves
    possible_moves = {}

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moves: list[str] = []

        self.captured_pieces: list[AbstractPiece] = []

        self.en_passant_takes = []

        self.board = _ChessBoard.from_fen(fen)

    def move(self, move: str) -> None:
        """ makes a move on the board

        Args:
            move (UCIMove): the move to move
        """
        self.moves.append(move)

        move = uci_into_coordinate_move(move)

        start_field_coordinates, target_field_coordinates = move

        moving_piece = self.board[start_field_coordinates]
        captured_piece = self.board[target_field_coordinates]

        self.captured_pieces.append(captured_piece)

        self.board[start_field_coordinates] = EmptyField.get_self()
        self.board[target_field_coordinates] = moving_piece

        en_passant_taken_piece = None
        if self.board.en_passant != "-" and moving_piece.lower_short == "p":
            took_en_passant = target_field_coordinates == uci_string_into_coordinate(self.board.en_passant)
            if took_en_passant:
                if self.whites_move():
                    en_passant_taken_piece = self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]]
                    self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]] = EmptyField.get_self()
                else:
                    en_passant_taken_piece = self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]]
                    self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]] = EmptyField.get_self()

        self.en_passant_takes.append(en_passant_taken_piece)
        self.board.en_passant = "-"

        y1, y2 = move[0][1], move[1][1]
        if moving_piece.lower_short == "p" and abs(y1 - y2) == 2:
            new_x = move[0][0]
            new_y = int(move[0][1] - ((move[0][1] - move[1][1]) / 2))
            self.board.en_passant = coordinate_into_uci_string((new_x, new_y))

    def unmove(self, move: str) -> None:
        """undoes a move on the board"""
        # removing the move to the array of moves
        self.moves.remove(move)
        # converting the UCIMove into a coordinate move
        move = uci_into_coordinate_move(move)

        start_field_coordinates, target_field_coordinates = move

        # getting the moved piece
        moved_piece = self.board[target_field_coordinates]
        captured_piece = self.captured_pieces.pop()
        # adding the moved piece to the startField
        self.board[start_field_coordinates] = moved_piece
        self.board[target_field_coordinates] = captured_piece

        en_passant_taken_piece = self.en_passant_takes.pop()
        if en_passant_taken_piece is not None:
            if self.whites_move():
                self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]] = en_passant_taken_piece
            else:
                self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]] = en_passant_taken_piece

    def whites_move(self) -> bool:
        """returns if it's white's move"""
        return len(self.moves) % 2 == 0

    class TestMove:
        """a class to test a move with the context manager"""

        def __init__(self, board: "ChessBoard", move: str):
            self.board = board
            self.move = move

        def __enter__(self) -> "ChessBoard":
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
        short_board = self.board.flat_short_board()
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
                    attacked_field: AbstractPiece = board.board[x, y]

                    if attacked_field.lower_short == "k" and attacked_field.is_white == for_white:
                        is_check = True
                        break

                if is_check:
                    remove_moves.append(move)

        for move in remove_moves:
            moves.remove(move)

        self.possible_moves[short_board] = moves

        return moves

    def generate_possible_coordinate_moves(self, for_white: bool | str) -> list[Move]:
        """ generates the possible coordinate moves for the passed color

        Args:
            for_white: the color of the pieces to generate the possible moves from

        Returns:
            returns all possible coordinate moves for the passed color
        """
        coordinate_moves = []
        # generating the color_board as a parameter for the generate_possible_coordinate_moves method of the pieces
        color_board = self.board.color_board()
        for p, piece in enumerate(self.board):
            coordinate = position_to_coordinate(p)

            # if the piece is the color for which to generate moves for
            if piece.is_white == for_white:
                # generating possible positions
                new_positions = piece.generate_possible_positions(coordinate,
                                                                  color_board)

                # append the new positions to the coordinate_moves
                coordinate_moves.extend((coordinate, new_position)
                                        for new_position in new_positions)
        return coordinate_moves

    def generate_fen_for_board(self) -> str:
        """ generates the fen for the current board

        Returns:
            string: the fen string for the current position on the board
        """
        fen = '/'.join([''.join([piece.short for piece in row]) for row in self.board])
        return fen

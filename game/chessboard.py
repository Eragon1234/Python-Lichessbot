from typing import Generator

from game._board import position_to_coordinate
from game._chessboard import _ChessBoard
from game.coordinate import Coordinate
from game.move import Move
from game.pieces import Piece, PieceType, Color


class ChessBoard:
    """Represents a chess board and provides ways to interact with it."""

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moves: list[str] = []

        self.captured_pieces: list[Piece] = []

        self.en_passant_takes = []

        self.board = _ChessBoard.from_fen(fen)

    def __hash__(self):
        return hash(self.board)

    def move(self, move: str) -> None:
        """
        makes a move on the board

        Args:
            move (UCIMove): the move to move
        """
        self.moves.append(move)

        move = Move.from_uci(move)

        start_field_coordinates, target_field_coordinates = move

        moving_piece = self.board[start_field_coordinates]
        captured_piece = self.board[target_field_coordinates]

        self.captured_pieces.append(captured_piece)

        self.board[start_field_coordinates] = Piece(PieceType.EMPTY, Color.EMPTY)
        self.board[target_field_coordinates] = moving_piece

        en_passant_taken_piece = None
        if self.board.en_passant != "-" and moving_piece.type == PieceType.PAWN:
            took_en_passant = target_field_coordinates == Coordinate.from_uci(self.board.en_passant)
            if took_en_passant:
                if self.whites_move():
                    en_passant_taken_piece = self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]]
                    self.board[target_field_coordinates[0] + 1, target_field_coordinates[1]] = Piece(PieceType.EMPTY,
                                                                                                     Color.EMPTY)
                else:
                    en_passant_taken_piece = self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]]
                    self.board[target_field_coordinates[0] - 1, target_field_coordinates[1]] = Piece(PieceType.EMPTY,
                                                                                                     Color.EMPTY)

        self.en_passant_takes.append(en_passant_taken_piece)
        self.board.en_passant = "-"

        y1, y2 = move[0][1], move[1][1]
        if moving_piece.type == PieceType.PAWN and abs(y1 - y2) == 2:
            new_x = move[0][0]
            new_y = int(move[0][1] - ((move[0][1] - move[1][1]) / 2))
            self.board.en_passant = Coordinate(new_x, new_y).uci()

    def unmove(self) -> None:
        """undoes the last move"""
        move = self.moves.pop()
        move = Move.from_uci(move)

        start_field_coordinates, target_field_coordinates = move

        moved_piece = self.board[target_field_coordinates]
        captured_piece = self.captured_pieces.pop()

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

        def __enter__(self):
            self.board.move(self.move)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.board.unmove()

    def test_move(self, move: str) -> TestMove:
        """returns an object that can be used to test a move with the context manager"""
        return self.TestMove(self, move)

    def generate_possible_moves(self, for_white: bool = True) -> Generator[str, None, None]:
        """
        Generating all possible moves in the current position

        Args:
            for_white (bool): for which color to generate the moves for.

        Returns:
            list: a list of possible moves in UCIMove format
        """
        coordinate_moves = self.generate_possible_coordinate_moves(for_white)

        moves = (move.uci() for move in coordinate_moves)

        for move in moves:
            with self.test_move(move):
                if self.king_in_check(for_white):
                    continue

                yield move

    def king_in_check(self, for_white: bool) -> bool:
        """
        returns if the king of the passed color is in check

        Args:
            for_white: the color of the king to check

        Returns:
            bool: if the king is in check
        """
        coordinate_moves = self.generate_possible_coordinate_moves(not for_white)

        for coordinate_move in coordinate_moves:
            target_coordinate = coordinate_move[1]
            attacked_field = self.board[target_coordinate]

            if attacked_field.type == PieceType.KING and attacked_field.is_white == for_white:
                return True

        return False

    def generate_possible_coordinate_moves(self, for_white: bool | str) -> Generator[Move, None, None]:
        """
        generates the possible coordinate moves for the passed color

        Args:
            for_white: the color of the pieces to generate the possible moves from

        Returns:
            returns all possible coordinate moves for the passed color
        """
        en_passant = None
        if self.board.en_passant != "-":
            en_passant = Coordinate.from_uci(self.board.en_passant)

        for position, piece in enumerate(self.board):
            if piece.is_white != for_white:
                continue

            coordinate = Coordinate(*position_to_coordinate(position))

            new_positions = piece.generate_possible_positions(self.board, coordinate, en_passant)

            yield from (Move(coordinate, new_position) for new_position in new_positions)

    def material_difference(self) -> int:
        """
        returns the difference in material

        Returns:
            int: the difference in material
        """
        return self.board.material_difference()

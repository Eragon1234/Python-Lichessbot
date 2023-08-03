from typing import Generator

from game._board import position_to_coordinate
from game._chessboard import _ChessBoard
from game.coordinate import Coordinate
from game.move import Move
from game.piece import Piece, PieceType, Color
from game.piece.move_groups import BACKWARD

UCI_MOVE_GENERATOR = Generator[str, None, None]
MOVE_GENERATOR = Generator[Move, None, None]


class ChessBoard:
    """Provides ways to interact with a chess board."""

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moves: list[Move] = []

        self.captured_pieces: list[Piece] = []

        self.en_passant_takes = []

        self.board = _ChessBoard.from_fen(fen)

    def __hash__(self):
        return hash(self.board)

    def move(self, move: Move | str) -> None:
        """
        makes a move on the board

        Args:
            move (Move): the move to move
        """
        if isinstance(move, str):
            move = Move.from_uci(move)

        self.moves.append(move)

        start_coordinates, target_coordinates = move

        moving_piece = self.board[start_coordinates]
        captured_piece = self.board[target_coordinates]

        self.captured_pieces.append(captured_piece)

        self.board[start_coordinates] = Piece(PieceType.EMPTY, Color.EMPTY)
        self.board[target_coordinates] = moving_piece

        en_passant_taken_piece = None
        if self.board.en_passant != "-" and moving_piece.type == PieceType.PAWN:
            en_passant_coordinate = Coordinate.from_uci(self.board.en_passant)
            took_en_passant = target_coordinates == en_passant_coordinate
            if took_en_passant:
                direction = 1 if self.whites_move() else -1
                took_coordinate = en_passant_coordinate + BACKWARD * direction
                en_passant_taken_piece = self.board[took_coordinate]

                empty_piece = Piece(PieceType.EMPTY, Color.EMPTY)
                self.board[took_coordinate] = empty_piece

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

        start_coordinates, target_coordinates = move

        moved_piece = self.board[target_coordinates]
        captured_piece = self.captured_pieces.pop()

        self.board[start_coordinates] = moved_piece
        self.board[target_coordinates] = captured_piece

        en_passant_taken_piece = self.en_passant_takes.pop()
        if en_passant_taken_piece is not None:
            direction = 1 if self.whites_move() else -1
            took_coordinate = target_coordinates + BACKWARD * direction
            self.board[took_coordinate] = en_passant_taken_piece

    def whites_move(self) -> bool:
        """returns if it's white's move"""
        return len(self.moves) % 2 == 0

    class TestMove:
        """a class to test a move with the context manager"""

        def __init__(self, board: "ChessBoard", move: Move):
            self.board = board
            self.move = move

        def __enter__(self):
            self.board.move(self.move)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.board.unmove()

    def test_move(self, move: Move) -> TestMove:
        """returns an object that can be used to test a move with the context manager"""
        return self.TestMove(self, move)

    def legal_moves(self, for_white: bool = True) -> MOVE_GENERATOR:
        """
        Generating all possible moves in the current position

        Args:
            for_white (bool): for which color to generate the moves for.

        Returns:
            list: a list of possible moves in UCIMove format
        """
        coordinate_moves = self.pseudo_legal_moves(for_white)

        for move in coordinate_moves:
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
        coordinate_moves = self.pseudo_legal_moves(not for_white)

        for coordinate_move in coordinate_moves:
            target_coordinate = coordinate_move[1]
            attacked_field = self.board[target_coordinate]

            if attacked_field.type == PieceType.KING and attacked_field.is_white == for_white:
                return True

        return False

    def pseudo_legal_moves(self, for_white: bool | str) -> MOVE_GENERATOR:
        """
        generates the pseudo legal moves for the passed color

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

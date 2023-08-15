from typing import Generator, Optional

from game._chessboard import _ChessBoard, position_to_coordinate
from game.coordinate import Coordinate
from game.move import Move
from game.piece import Piece, PieceType, Color
from game.piece.move_groups import BACKWARD

UciMoveGenerator = Generator[str, None, None]
MoveGenerator = Generator[Move, None, None]


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

        move: Move

        self.moves.append(move)

        moving_piece = self.board.pop(move.start_field)
        if move.promote_to is not None:
            moving_piece = Piece(move.promote_to, moving_piece.color)

        self.captured_pieces.append(self.board[move.target_field])

        self.board[move.target_field] = moving_piece

        en_passant_coordinate = self.get_en_passant_capture(move)
        if en_passant_coordinate is not None:
            self.en_passant_takes.append(self.board.pop(en_passant_coordinate))
        else:
            self.en_passant_takes.append(None)

        self.board.en_passant = self.new_en_passant_coordinate(move)

    def get_en_passant_capture(self, move: Move) -> Optional[Coordinate]:
        """
        returns the coordinate of the pawn that was taken en passant
        if no pawn was taken en passant, returns None

        Args:
            move: the move to check

        Returns:
            Coordinate: the coordinate of the pawn that was taken en passant
        """
        moving_piece = self.board[move.start_field]

        if moving_piece.type is not PieceType.PAWN:
            return None

        if self.board.en_passant == "-":
            return None

        en_passant_coordinate = Coordinate.from_uci(self.board.en_passant)
        if move.target_field != en_passant_coordinate:
            return None

        direction = 1 if moving_piece.color is Color.WHITE else -1
        return move.target_field + BACKWARD * direction

    def new_en_passant_coordinate(self, move: Move) -> str:
        """
        returns the uci coordinate where a pawn can be taken en passant
        if no pawn was taken en passant, returns '-'

        Args:
            move: the move to check

        Returns:
            str: the uci coordinate where a pawn can be taken en passant
        """
        moving_piece = self.board[move.start_field]
        if moving_piece.type is not PieceType.PAWN:
            return "-"

        move_difference = abs(move.start_field.y - move.target_field.y)
        if move_difference != 2:
            return "-"

        en_passant_rank = 2 if moving_piece.color is Color.WHITE else 5
        return Coordinate(move.target_field.x, en_passant_rank).uci()

    def unmove(self) -> None:
        """undoes the last move"""
        move = self.moves.pop()

        moved_piece = self.board[move.target_field]
        if move.promote_to is not None:
            moved_piece = Piece(PieceType.PAWN, moved_piece.color)
        captured_piece = self.captured_pieces.pop()

        self.board[move.start_field] = moved_piece
        self.board[move.target_field] = captured_piece

        en_passant_taken_piece = self.en_passant_takes.pop()
        if en_passant_taken_piece is not None:
            en_passant_coordinate = self.get_en_passant_capture(move)
            self.board[en_passant_coordinate] = en_passant_taken_piece

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
        """Returns a context manager to test a move."""
        return self.TestMove(self, move)

    def legal_moves(self, color: Color) -> MoveGenerator:
        """
        Generating all possible moves in the current position

        Args:
            color: for which color to generate the moves for.

        Returns:
            MoveGenerator: a generator for all possible moves
        """
        moves = self.pseudo_legal_moves(color)

        for move in moves:
            with self.test_move(move):
                if self.king_in_check(color):
                    continue

            yield move

    def king_in_check(self, color: Color) -> bool:
        """
        returns if the king of the passed color is in check

        Args:
            color: the color of the king to check

        Returns:
            bool: if the king is in check
        """
        moves = self.pseudo_legal_moves(color.enemy())

        for move in moves:
            attacked_field = self.board[move.target_field]

            if attacked_field.color is not color:
                continue

            if attacked_field.type is PieceType.KING:
                return True

        return False

    def pseudo_legal_moves(self, color: Color) -> MoveGenerator:
        """
        generates the pseudo legal moves for the passed color

        Args:
            color: the color to generate the moves for

        Returns:
            returns all possible moves for the passed color
        """
        en_passant = None
        if self.board.en_passant != "-":
            en_passant = Coordinate.from_uci(self.board.en_passant)

        for position, piece in enumerate(self.board):
            if piece.color is not color:
                continue

            coordinate = Coordinate(*position_to_coordinate(position))

            new_positions = piece.moves(self.board, coordinate, en_passant)

            yield from new_positions

    def material_difference(self) -> int:
        """
        returns the difference in material

        Returns:
            int: the difference in material
        """
        return self.board.material_difference()

    def fen(self) -> str:
        """
        returns the fen of the board

        Returns:
            str: the fen of the board
        """
        return self.board.fen()

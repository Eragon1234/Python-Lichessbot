from typing import Generator

from game._chessboard import _ChessBoard, position_to_coordinate
from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.move.move import Move
from game.move.uci import move_from_uci
from game.piece.color import Color
from game.piece.move_groups import BACKWARD
from game.piece.piece import Piece
from game.piece.piece_type import PieceType

UciMoveGenerator = Generator[str, None, None]
MoveGenerator = Generator[Move, None, None]


class ChessBoard:
    """Provides ways to interact with a chess board."""

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moves: list[Move] = []

        self.captured_pieces: list[Piece] = []

        self.en_passant: list[str] = []
        self.castling_rights: list[CastlingRights] = []
        self.en_passant_takes = []

        self.board = _ChessBoard.from_fen(fen)

    def __hash__(self):
        return hash(self.board)

    def move(self, move: Move | str) -> None:
        """
        makes a move on the board

        Args:
            move: the move to move
        """
        if isinstance(move, str):
            move = move_from_uci(self.board, move)

        move: Move

        self.moves.append(move)

        move.move(self.board)

    def unmove(self) -> None:
        """undoes the last move"""
        move = self.moves.pop()

        move.undo(self.board)

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
            if self.is_castle(move):
                if self.king_in_check(color):
                    continue
                if self.is_attacked(self.castles_trough(move), color.enemy()):
                    continue
            with self.test_move(move):
                if self.king_in_check(color):
                    continue

            yield move

    def is_castle(self, move: Move) -> bool:
        """
        returns if the move is a castle
        Args:
            move: the move to check

        Returns:
            bool: if the move is a castle
        """
        if not self.board[move.start_field].type is PieceType.KING:
            return False

        return self.is_kingside_castle(move) or self.is_queenside_castle(move)

    @staticmethod
    def is_kingside_castle(move: Move) -> bool:
        """
        returns if the move is a kingside castle
        assumes that the moving piece is a king
        Args:
            move: thte move to check

        Returns:
            bool: if the move is a kingside castle
        """
        return move.start_field.x - move.target_field.x == 2

    @staticmethod
    def is_queenside_castle(move: Move) -> bool:
        """
        returns if the move is a queenside castle
        assumes that the moving piece is a king
        Args:
            move: the move to check

        Returns:
            bool: if the move is a queenside castle
        """
        return move.start_field.x - move.target_field.x == -2

    @staticmethod
    def castles_trough(move: Move) -> Coordinate:
        """
        returns the coordinate the king moves trough when castling
        It is assumed that the move is a castle

        Args:
            move: the move to check

        Returns:
            Coordinate: the coordinate the king moves trough when castling
        """
        direction = 1 if move.start_field.x < move.target_field.x else -1
        return move.start_field + BACKWARD * direction

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

    def is_attacked(self, pos: Coordinate, color: Color) -> bool:
        """
        returns if the passed position is attacked by the passed color

        Args:
            pos: the position to check
            color: the color to check

        Returns:
            bool: if the position is attacked
        """
        moves = self.pseudo_legal_moves(color)

        for move in moves:
            if move.target_field == pos:
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

            moves = piece.moves(self.board, coordinate, en_passant,
                                self.board.castling_rights)

            yield from moves

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

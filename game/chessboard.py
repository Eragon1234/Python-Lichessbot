from collections.abc import Iterator

from game.board import Board, coordinates
from game.coordinate import Coordinate
from game.move import CastleMove
from game.move.move import Move
from game.move.uci import move_from_uci
from game.piece.color import Color
from game.piece.move_groups import BACKWARD
from game.piece.piece_type import PieceType

MoveIterator = Iterator[Move]


class ChessBoard:
    """Provides ways to interact with a chess board."""

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moves: list[Move] = []

        self._board = Board.from_fen(fen)

    def __hash__(self):
        return hash(self._board)

    def move(self, move: Move | str) -> None:
        """
        makes a move on the board

        Args:
            move: the move to move
        """
        if isinstance(move, str):
            move = move_from_uci(self._board, move)

        move: Move

        self.moves.append(move)

        move.move(self._board)

    def unmove(self) -> None:
        """undoes the last move"""
        move = self.moves.pop()

        move.undo(self._board)

    def whites_move(self) -> bool:
        """returns if it's white's move"""
        return self._board.turn is Color.WHITE

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

    def legal_moves(self) -> MoveIterator:
        """
        Generating all possible moves in the current position

        Returns:
            A generator object that yields all possible moves.
        """
        color = self._board.turn
        
        moves = self.pseudo_legal_moves(color)

        for move in moves:
            if isinstance(move, CastleMove):
                if self.king_in_check(color):
                    continue
                if self.is_attacked(self.castles_trough(move), color.enemy()):
                    continue
            with self.test_move(move):
                if self.king_in_check(color):
                    continue

            yield move

    @staticmethod
    def castles_trough(move: Move) -> Coordinate:
        """
        returns the coordinate the king moves through when castling
        It is assumed that the move is a castle

        Args:
            move: the move to check

        Returns:
            Coordinate: the coordinate the king moves through when castling
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
            attacked_field = self._board[move.target_field]

            if attacked_field.color is not color:
                continue

            if attacked_field.type is PieceType.KING:
                return True

        return False

    def is_attacked(self, pos: Coordinate, color: Color) -> bool:
        """
        returns if the passed color attacks the passed position

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

    def pseudo_legal_moves(self, color: Color) -> MoveIterator:
        """
        generates the pseudo legal moves for the passed color

        Args:
            color: the color to generate the moves for

        Returns:
            returns all possible moves for the passed color
        """
        for coordinate in coordinates:
            if not self._board.is_type(coordinate.value, PieceType.WHITE if color is Color.WHITE else PieceType.BLACK):
                continue

            piece = self._board[coordinate]
            moves = piece.moves(self._board, coordinate,
                                self._board.en_passant,
                                self._board.castling_rights)

            yield from moves

    def material_difference(self) -> int:
        """
        returns the difference in material

        Returns:
            int: the difference in material
        """
        return self._board.material_difference()

    def value_at(self, coordinate: Coordinate) -> int:
        """
        returns the value of the piece at the passed coordinate

        Args:
            coordinate: the coordinate to check

        Returns:
            int: the value of the piece at the passed coordinate
        """
        return self._board[coordinate].value

    def fen(self) -> str:
        """
        returns the fen of the board

        Returns:
            str: the fen of the board
        """
        return self._board.fen()

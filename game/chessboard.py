from collections.abc import Iterator

from game.board import Board, coordinates
from game.coordinate import Coordinate
from game.move import castle_move, Move, factory
from game.move.uci import move_from_uci
from game.piece import generate_moves
from game.piece.color import Color
from game.piece.move_groups import BACKWARD
from game.piece.piece_type import PieceType

MoveIterator = Iterator[Move]


class ChessBoard:
    """Provides ways to interact with a chess board."""

    def __init__(self, fen: str = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moves: list[Move] = []

        self._board = Board.from_fen(fen)
        self._previous_boards = []

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

        self._previous_boards.append(self._board)

        self._board = self._board.clone()

        move.move(self._board)

    def is_valid_move(self, move: Move | str) -> bool:
        if isinstance(move, Move):
            move = move.uci()

        return move in (m.uci() for m in self.legal_moves())

    def is_threefold_repetition(self) -> bool:
        return self._previous_boards.count(self._board) >= 2

    def unmove(self) -> None:
        """undoes the last move"""
        self.moves.pop()

        self._board = self._previous_boards.pop()

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
            if move.func is castle_move:
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
        color = PieceType.WHITE if color is Color.WHITE else PieceType.BLACK

        king_pos = next(coordinate for coordinate in coordinates if self._board[coordinate] is PieceType.KING | color)

        knight_moves = generate_moves(PieceType.KNIGHT | color, factory, self._board, king_pos)
        for move in knight_moves:
            if self._board.is_type(move.target_field, PieceType.KNIGHT):
                return True

        bishop_moves = generate_moves(PieceType.BISHOP | color, factory, self._board, king_pos)
        for move in bishop_moves:
            if self._board.is_type(move.target_field, PieceType.BISHOP) or self._board.is_type(move.target_field,
                                                                                               PieceType.QUEEN):
                return True

        rook_moves = generate_moves(PieceType.ROOK | color, factory, self._board, king_pos)
        for move in rook_moves:
            if self._board.is_type(move.target_field, PieceType.ROOK) or self._board.is_type(move.target_field,
                                                                                             PieceType.QUEEN):
                return True

        pawn_moves = generate_moves(PieceType.PAWN | color, factory, self._board, king_pos)
        for move in pawn_moves:
            if self._board.is_type(move.target_field, PieceType.PAWN):
                return True

        king_moves = generate_moves(PieceType.KING | color, factory, self._board, king_pos)
        for move in king_moves:
            if self._board.is_type(move.target_field, PieceType.KING):
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
            if not self._board.is_type(coordinate, PieceType.WHITE if color is Color.WHITE else PieceType.BLACK):
                continue

            piece_type = self._board[coordinate]
            moves = generate_moves(piece_type, factory, self._board, coordinate)
            yield from moves

    def material_difference(self) -> int:
        """
        returns the difference in material

        Returns:
            int: the difference in material
        """
        return self._board.value

    def value_at(self, coordinate: Coordinate) -> int:
        """
        returns the value of the piece at the passed coordinate

        Args:
            coordinate: the coordinate to check

        Returns:
            int: the value of the piece at the passed coordinate
        """
        return self._board[coordinate].value_at(coordinate)

    def fen(self) -> str:
        """
        returns the fen of the board

        Returns:
            str: the fen of the board
        """
        return self._board.fen()

    def approximate_board_state(self) -> int:
        return self._board.approximate_board_state()

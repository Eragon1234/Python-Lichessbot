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

        self.moves.append(move)

        start_coordinates, target_coordinates = move

        moving_piece = self.board[start_coordinates]
        captured_piece = self.board[target_coordinates]

        self.captured_pieces.append(captured_piece)

        self.board[start_coordinates] = Piece(PieceType.EMPTY, Color.EMPTY)
        self.board[target_coordinates] = moving_piece

        en_passant_coordinate = self.en_passant(move)
        en_passant_taken_piece = None
        if en_passant_coordinate is not None:
            en_passant_taken_piece = self.board[en_passant_coordinate]

            empty_piece = Piece(PieceType.EMPTY, Color.EMPTY)
            self.board[en_passant_coordinate] = empty_piece

        self.en_passant_takes.append(en_passant_taken_piece)
        self.board.en_passant = "-"

        new_en_passant_coordinate = self.new_en_passant_coordinate(move)
        if new_en_passant_coordinate is not None:
            self.board.en_passant = new_en_passant_coordinate.uci()

    def en_passant(self, move: Move) -> Optional[Coordinate]:
        """
        returns the coordinate of the pawn that was taken en passant
        if no pawn was taken en passant, returns None

        Args:
            move: the move to check

        Returns:
            Coordinate: the coordinate of the pawn that was taken en passant
        """
        start_coordinate, target_coordinate = move

        moving_piece = self.board[start_coordinate]
        if moving_piece.type != PieceType.PAWN:
            return None

        could_move_en_passant = self.board.en_passant != "-"
        if not could_move_en_passant:
            return None

        en_passant_coordinate = Coordinate.from_uci(self.board.en_passant)
        took_en_passant = target_coordinate == en_passant_coordinate
        if not took_en_passant:
            return None

        direction = 1 if self.whites_move() else -1
        return target_coordinate + BACKWARD * direction

    def new_en_passant_coordinate(self, move: Move) -> Optional[Coordinate]:
        """
        returns the coordinate where a pawn can be taken en passant
        if no pawn was taken en passant, returns None

        Args:
            move: the move to check

        Returns:
            Coordinate: the coordinate where a pawn could move to en passant
        """
        start_coordinate, target_coordinate = move

        moving_piece = self.board[start_coordinate]
        if moving_piece.type != PieceType.PAWN:
            return None

        move_difference = abs(start_coordinate.y - target_coordinate.y)
        if move_difference != 2:
            return None

        en_passant_rank = 2 if moving_piece.color == Color.WHITE else 5
        return Coordinate(target_coordinate.x, en_passant_rank)



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
        """Returns a context manager to test a move."""
        return self.TestMove(self, move)

    def legal_moves(self, color: Color) -> MoveGenerator:
        """
        Generating all possible moves in the current position

        Args:
            color: for which color to generate the moves for.

        Returns:
            list: a list of possible moves in UCIMove format
        """
        coordinate_moves = self.pseudo_legal_moves(color)

        for move in coordinate_moves:
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
        coordinate_moves = self.pseudo_legal_moves(color.enemy())

        for coordinate_move in coordinate_moves:
            target_coordinate = coordinate_move[1]
            attacked_field = self.board[target_coordinate]

            if attacked_field.color != color:
                continue

            if attacked_field.type == PieceType.KING:
                return True

        return False

    def pseudo_legal_moves(self, color: Color) -> MoveGenerator:
        """
        generates the pseudo legal moves for the passed color

        Args:
            color: the color to generate the moves for

        Returns:
            returns all possible coordinate moves for the passed color
        """
        en_passant = None
        if self.board.en_passant != "-":
            en_passant = Coordinate.from_uci(self.board.en_passant)

        for position, piece in enumerate(self.board):
            if piece.color != color:
                continue

            coordinate = Coordinate(*position_to_coordinate(position))

            new_positions = piece.positions(self.board, coordinate, en_passant)

            yield from (Move(coordinate, new_position)
                        for new_position in new_positions)

    def material_difference(self) -> int:
        """
        returns the difference in material

        Returns:
            int: the difference in material
        """
        return self.board.material_difference()

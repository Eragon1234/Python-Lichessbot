from typing import Generator, Optional

from game.coordinate import Coordinate
from game.move import Move
from game.piece.board import Board
from game.piece.bonus import BONUS_MAPS
from game.piece.color import Color
from game.piece.move_groups import MOVE_GROUPS, FORWARD, LEFT, RIGHT
from game.piece.piece_type import PieceType
from game.piece.values import VALUES

MoveGenerator = Generator[Move, None, None]
PROMOTE_TYPES = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP,
                 PieceType.KNIGHT]


class Piece:
    """
    A piece on a chess board.
    The type attribute specifies the type of the piece.
    The piece can also represent an empty field.
    """

    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type

        self.color = color

        self.value = VALUES[self.type]
        if self.color is Color.BLACK:
            self.value = -self.value

        self.legal_target_colors = self.color.enemy() | Color.EMPTY

        self.possible_move_groups = MOVE_GROUPS[self.type]

        self.bonus_map = BONUS_MAPS[self.type]

    def move_to(self, position: tuple[int, int]):
        bonus = self.bonus_map[position[1]][position[0]]
        self.value = VALUES[self.type] + bonus
        if self.color is Color.BLACK:
            self.value = -self.value

    @classmethod
    def from_fen(cls, fen: str) -> 'Piece':
        """
        Creates a piece from a FEN string.

        Args:
            fen: The FEN string.

        Returns:
            A piece object.
        """
        color = Color.WHITE if not fen.islower() else Color.BLACK
        fen = fen.lower()

        return cls(PieceType(fen), color)

    def fen(self) -> str:
        """
        Returns:
            The FEN string for the piece.
        """
        short = self.type.value
        if self.color is Color.WHITE:
            short = short.upper()
        return short

    def is_legal_target(self, board: Board, position: Coordinate,
                        legal_target_colors: Optional[Color] = None) -> bool:
        """
        Checks if a given position on the board is a legal target for a piece.

        Args:
            board (Board): The game board.
            position (Coordinate): The position to check.
            legal_target_colors (Optional[Color]): The legal target colors.

        Returns:
            bool: whether the position is a legal target.
        """
        if legal_target_colors is None:
            legal_target_colors = self.legal_target_colors

        x, y = position

        if x < 0 or x > 7 or y < 0 or y > 7:
            return False

        return board.color_at(position) in legal_target_colors

    def moves(self, board: Board, pos: Coordinate,
              en_passant: Optional[Coordinate] = None) -> MoveGenerator:
        """
        Generates possible moves for a piece on the given chess board.

        Args:
            board: The chess board.
            pos: The current position of the piece.
            en_passant: Optional en passant position.

        Returns:
            A generator object that yields possible moves for the piece.
        """
        if self.type is PieceType.PAWN:
            return self._moves_for_pawn(board, pos, en_passant)

        return self._moves_with_move_groups(board, pos)

    def _moves_with_move_groups(self, board: Board,
                                pos: Coordinate) -> MoveGenerator:
        """
        Generates possible moves for a piece on the given chess board.

        Args:
            board: The chess board.
            pos: The current position of the piece.

        Returns:
            A generator object that yields possible moves for the piece.
        """
        for move_group in self.possible_move_groups:
            for move in move_group:
                new_pos = pos + move

                if not self.is_legal_target(board, new_pos):
                    break

                yield Move(pos, new_pos)

                target_field_color = board.color_at(new_pos)
                if target_field_color is not Color.EMPTY:
                    break

    def _moves_for_pawn(self, board: Board, pos: Coordinate,
                        en_passant: Optional[Coordinate] = None) -> MoveGenerator:
        """
        Generates possible moves for a pawn on the given chess board.

        Args:
            board: The chess board.
            pos: The current position of the pawn.
            en_passant: The position where a pawn could move en passant.

        Returns:
            A generator object that yields possible moves for the pawn.
        """
        promote = self.is_start_rank(pos, self.color.enemy())
        for target in self._positions_for_pawn(board, pos, en_passant):
            if not promote:
                yield Move(pos, target)
                continue

            for piece_type in PROMOTE_TYPES:
                yield Move(pos, target, piece_type)

    def _positions_for_pawn(self, board: Board, pos: Coordinate,
                            en_passant: Optional[Coordinate] = None) -> Generator[Coordinate, None, None]:
        """
        Generates possible positions for a pawn on the given chess board.
        """
        forward = FORWARD
        if self.color is Color.BLACK:
            forward = -forward

        possible_target = pos + forward
        if self.is_legal_target(board, possible_target, Color.EMPTY):
            yield possible_target

            if self.is_start_rank(pos):
                possible_target = pos + 2 * forward
                if self.is_legal_target(board, possible_target, Color.EMPTY):
                    yield possible_target

        possible_target = pos + LEFT + forward
        if self.is_legal_target(board, possible_target, self.color.enemy()):
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

        possible_target = pos + RIGHT + forward
        if self.is_legal_target(board, possible_target, self.color.enemy()):
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

    def is_start_rank(self, pos: Coordinate,
                      color: Optional[Color] = None) -> bool:
        """
        Checks if a given position is the start rank for a pawn of the color.

        Args:
            pos: The position to check.
            color: The color of the pawn. Defaults to the color of the piece.

        Returns:
            bool: whether the position is the start rank for a pawn.
        """
        if color is None:
            color = self.color
        start_rank = 1 if color is Color.WHITE else 6
        return pos[1] == start_rank

from typing import Generator, Optional

from game.coordinate import Coordinate
from game.piece.board import Board
from game.piece.color import Color
from game.piece.move_groups import POSSIBLE_MOVE_GROUPS, FORWARD, LEFT, RIGHT
from game.piece.piece_type import PieceType
from game.piece.values import VALUES

PositionGenerator = Generator[Coordinate, None, None]


class Piece:
    """
    A piece on a chess board.
    The type of the piece is specified by the type attribute.
    The piece can also represent an empty field.
    """

    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type

        self.color = color

        if self.color == Color.EMPTY:
            self.is_white = "EmptyField"
        else:
            self.is_white = self.color == Color.WHITE

        self.short = self.type.value
        if self.is_white:
            self.short = self.short.upper()

        self.direction_multiplier = 1 if self.is_white else -1

        self.value = VALUES[self.type] * self.direction_multiplier

        self.legal_target_colors = self.color.enemy_color() | Color.EMPTY

        self.possible_move_groups = POSSIBLE_MOVE_GROUPS[self.type]

    @classmethod
    def from_fen(cls, fen: str) -> 'Piece':
        white = Color.WHITE if not fen.islower() else Color.BLACK
        fen = fen.lower()

        return cls(PieceType(fen), white)

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

        if (0 > x or x > 7) or (0 > y or y > 7):
            return False

        target_field_color = board.color_at(position)
        return target_field_color in legal_target_colors

    def generate_possible_positions(self, board: Board,
                                    current_position: Coordinate,
                                    en_passant: Optional[Coordinate] = None) -> PositionGenerator:
        """
        Generates possible positions for a piece on the given chess board.

        Args:
            board: The chess board.
            current_position: The current position of the piece.
            en_passant: Optional en passant position.

        Returns:
            A generator object that yields possible positions for the piece.
        """
        if self.type == PieceType.PAWN:
            yield from self._generate_possible_positions_for_pawn(board, current_position, en_passant)
        else:
            yield from self._generate_possible_positions_with_move_groups(board, current_position)

    def _generate_possible_positions_with_move_groups(self, board: Board,
                                                      current_position: Coordinate) -> PositionGenerator:
        for move_group in self.possible_move_groups:
            for move in move_group:
                pos = current_position + move

                if not self.is_legal_target(board, pos):
                    break

                yield pos

                target_field_color = board.color_at(pos)
                if target_field_color is not Color.EMPTY:
                    break

    def _generate_possible_positions_for_pawn(self, board: Board,
                                              pos: Coordinate,
                                              en_passant: Optional[Coordinate] = None) -> PositionGenerator:
        forward = FORWARD * self.direction_multiplier
        possible_target = pos + forward
        if self.is_legal_target(board, possible_target, Color.EMPTY):
            yield possible_target

            if self.is_start_rank(pos):
                possible_target = pos + 2 * forward
                if self.is_legal_target(board, possible_target, Color.EMPTY):
                    yield possible_target

        possible_target = pos + LEFT + forward
        if self.is_legal_target(board, possible_target, self.color.enemy_color()):
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

        possible_target = pos + RIGHT + forward
        if self.is_legal_target(board, possible_target, self.color.enemy_color()):
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

    def is_start_rank(self, pos: Coordinate):
        return pos[1] == (1 if self.is_white else 6)

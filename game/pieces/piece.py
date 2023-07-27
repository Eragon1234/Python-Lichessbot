from typing import Generator, Optional

from game.pieces.board import Board
from game.pieces.color import Color
from game.pieces.move_groups import POSSIBLE_MOVE_GROUPS
from game.pieces.piece_type import PieceType
from game.pieces.values import VALUES
from game.types import Position


class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type

        self.color = color

        self.is_white = "EmptyField" if self.type == PieceType.EMPTY else self.color == Color.WHITE

        self.short = self.type.value
        if self.is_white:
            self.short = self.short.upper()

        self.direction_multiplier = 1 if self.is_white else -1

        self.value = VALUES[self.type] * self.direction_multiplier

        self.legal_target_colors = {
            self.color.enemy_color(),
            Color.EMPTY
        }

        self.possible_move_groups = POSSIBLE_MOVE_GROUPS[self.type]

    def is_legal_target(self, board: Board, position: Position,
                        legal_target_colors: set[Color] = None) -> bool:
        if legal_target_colors is None:
            legal_target_colors = self.legal_target_colors

        x, y = position

        if (0 > x or x > 7) or (0 > y or y > 7):
            return False

        target_field_color = board.color_at(position)
        return target_field_color in legal_target_colors

    def generate_possible_positions(self, board: Board,
                                    current_position: Position,
                                    en_passant: Optional[Position] = None) -> Generator[Position, None, None]:
        if self.type == PieceType.PAWN:
            yield from self._generate_possible_positions_for_pawn(board, current_position, en_passant)
        else:
            yield from self._generate_possible_positions_with_move_groups(board, current_position)

    def _generate_possible_positions_with_move_groups(self, board: Board, current_position: Position) -> Generator[
        Position, None, None]:
        for move_groups in self.possible_move_groups:
            for move in move_groups:
                pos = (
                    current_position[0] + move[0],
                    current_position[1] + move[1]
                )
                if not self.is_legal_target(board, pos):
                    break

                yield pos

                target_field_color = board.color_at(pos)
                if target_field_color == self.color.enemy_color() and target_field_color != Color.EMPTY:
                    break

    def _generate_possible_positions_for_pawn(self, board: Board,
                                              current_position: Position,
                                              en_passant: Optional[Position] = None) -> Generator[Position, None, None]:
        x, y = current_position

        possible_target = (x, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {Color.EMPTY}):
            yield possible_target

            if self.is_start_rank(current_position):
                possible_target = (x, y + 2 * self.direction_multiplier)
                if self.is_legal_target(board, possible_target, {Color.EMPTY}):
                    yield possible_target

        possible_target = (x + 1, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {self.color.enemy_color()}):
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

        possible_target = (x - 1, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {self.color.enemy_color()}):
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

    def is_start_rank(self, pos: Position):
        return pos[1] == (1 if self.is_white else 6)

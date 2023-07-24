from typing import Generator

from game.pieces.values import VALUES
from game.pieces.color import Color
from game.pieces.move_groups import POSSIBLE_MOVE_GROUPS
from game.pieces.piece_type import PieceType
from game.types import BoardArray, Position


class Piece:
    def __init__(self, piece_type: PieceType, is_white: bool | str):
        self.type = piece_type

        self.color = Color.WHITE if is_white else Color.BLACK
        if self.type == PieceType.EMPTY:
            self.color = Color.EMPTY

        self.direction_multiplier = 1 if is_white else -1

        self.legal_target_colors = {
            not self.is_white,
            'EmptyField'
        }

    @property
    def short(self):
        short = self.type.value
        if self.is_white:
            short = short.upper()
        return short

    @property
    def is_white(self) -> bool | str:
        return "EmptyField" if self.type == PieceType.EMPTY else self.color == Color.WHITE

    @property
    def value(self):
        return VALUES[self.type] * self.direction_multiplier

    @property
    def possible_move_groups(self) -> list[list[tuple[int, int]]]:
        return POSSIBLE_MOVE_GROUPS[self.type]

    def is_legal_target(self, board: BoardArray, position: Position,
                        legal_target_colors: set[bool | str] = None) -> bool:
        if legal_target_colors is None:
            legal_target_colors = self.legal_target_colors

        x, y = position

        if (0 > x or x > 7) or (0 > y or y > 7):
            return False

        target_field_color = board[x, y]
        return target_field_color in legal_target_colors

    def generate_possible_positions(self, board: BoardArray, current_position: Position) -> Generator[Position, None, None]:
        if self.type == PieceType.PAWN:
            yield from self._generate_possible_positions_for_pawn(board, current_position)
        else:
            yield from self._generate_possible_positions_with_move_groups(board, current_position)

    def _generate_possible_positions_with_move_groups(self, board: BoardArray, current_position: Position) -> Generator[Position, None, None]:
        for move_groups in self.possible_move_groups:
            for move in move_groups:
                pos = (
                    current_position[0] + move[0],
                    current_position[1] + move[1]
                )
                if not self.is_legal_target(board, pos):
                    break

                yield pos

                if board[pos] == (not self.is_white) and board[pos] != 'EmptyField':
                    break

    def _generate_possible_positions_for_pawn(self, board: BoardArray, current_position: Position) -> Generator[Position, None, None]:
        x, y = current_position

        possible_target = (x, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {"EmptyField"}):
            yield possible_target

            if self.is_start_rank(current_position):
                possible_target = (x, y + 2 * self.direction_multiplier)
                if self.is_legal_target(board, possible_target, {"EmptyField"}):
                    yield possible_target

        possible_target = (x + 1, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {not self.is_white, "enemy"}):
            yield possible_target

        possible_target = (x - 1, y + 1 * self.direction_multiplier)
        if self.is_legal_target(board, possible_target, {not self.is_white, "enemy"}):
            yield possible_target

    def is_start_rank(self, pos: Position):
        return pos[1] == (1 if self.is_white else 6)

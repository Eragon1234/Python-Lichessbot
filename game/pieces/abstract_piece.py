import abc

from game.types import BoardArray, Position, Coordinate


class AbstractPiece(abc.ABC):
    lower_short = 'e'
    value = 0
    bonus_map = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    possible_move_groups: list[list[Coordinate]] = []

    def __init__(self, is_white: bool | str):
        self.is_white = is_white
        self.short = self.lower_short.upper() if is_white else self.lower_short
        self.direction_multiplier = 1 if is_white else -1
        if not is_white:
            self.value = -self.value

        self.target_field_conditions = {
            not self.is_white,
            'EmptyField'
        }

    def is_legal_target(self, board: BoardArray, position: Position,
                        target_field_conditions: set[bool | str] = None) -> bool:
        if target_field_conditions is None:
            target_field_conditions = self.target_field_conditions

        x, y = position

        if (0 > x or x > 7) or (0 > y or y > 7):
            return False

        target_field = board[x, y]
        return target_field in target_field_conditions

    def generate_possible_positions(self, current_position: Position, board: BoardArray) -> list[Position]:
        possible_positions = []
        for move_groups in self.possible_move_groups:
            for move in move_groups:
                x = current_position[0] + move[0]
                y = current_position[1] + move[1]
                if self.is_legal_target(board, (x, y)):
                    possible_positions.append((x, y))
                else:
                    break

                if board[x, y] == (not self.is_white) and board[x, y] != 'EmptyField':
                    break
        return possible_positions

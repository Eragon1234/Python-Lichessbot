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

    def check_if_position_is_legal(self, board: BoardArray, positions: list[Position], x: int, y: int,
                                   target_field_conditions: set[bool | str] = None) -> bool:
        if target_field_conditions is None:
            target_field_conditions = self.target_field_conditions

        if 0 <= x <= 7 and 0 <= y <= 7:
            position = (x, y)
            target_field = board[position]
            if target_field in target_field_conditions:
                positions.append(position)
                return True
        return False

    def generate_possible_positions(self, current_position: Position, board: BoardArray) -> list[Position]:
        possible_positions = []
        for move_groups in self.possible_move_groups:
            for move in move_groups:
                x = current_position[0] + move[0]
                y = current_position[1] + move[1]
                if not self.check_if_position_is_legal(board, possible_positions, x, y):
                    break
                if board[x, y] == (not self.is_white) and board[x, y] != 'EmptyField':
                    break
        return possible_positions

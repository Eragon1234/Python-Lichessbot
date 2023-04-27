import abc

from game.pieces.types import BoardArray, Positions, Position


class AbstractPiece(abc.ABC):
    position = (0, 0)
    short = 'e'
    value = 0
    positions = []
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

    def __init__(self, is_white: bool | str):
        self.lower_short = self.short
        self.is_white = is_white
        if self.is_white:
            self.short = self.short.upper()
            self.direction_multiplier = 1
        else:
            self.value = self.value * -1
            self.direction_multiplier = -1

        self.target_field_conditions = [
            not self.is_white,
            'EmptyField'
        ]

    def check_if_position_is_legal(self, board: BoardArray, positions: Positions, x: int, y: int,
                                   target_field_conditions: bool = False) -> bool:
        if not target_field_conditions:
            target_field_conditions = self.target_field_conditions
        if 0 <= x <= 7 and 0 <= y <= 7:
            position = (x, y)
            target_field = board[y][x]
            for condition in target_field_conditions:
                if target_field == condition:
                    positions.append(position)
                    return condition
        return False

    @staticmethod
    def filter_positions(positions: Positions) -> Positions:
        return [position for position in positions if 0 <= position[0] <= 7 and 0 <= position[1] <= 7]

    @abc.abstractmethod
    def generate_possible_positions(self, current_position: Position, board: BoardArray):
        pass

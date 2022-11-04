import abc
import numpy as np


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

    def __init__(self, is_white: bool):
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

        self.bonus_map = np.array(self.bonus_map)

    def check_if_position_is_legal(self, board: list[list[str]], positions: list[tuple[int, int]], x: int, y: int,
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

    @staticmethod
    def filter_positions(positions: list[tuple]) -> list[tuple[int, int]]:
        return list(filter(lambda position: 0 <= position[0] <= 7 and 0 <= position[1] <= 7, positions))

    @abc.abstractmethod
    def generate_possible_positions(self, current_position: tuple[int, int], board: list[list[str]]):
        pass

    def get_value(self) -> int:
        return self.value

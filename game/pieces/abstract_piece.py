import abc
from typing import Tuple, List

from game.pieces.types import BoardArray, Positions, Position


class AbstractPiece(abc.ABC):
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

    possible_move_groups: List[List[Tuple[int, int]]] = []

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
                                   target_field_conditions: list[bool | str] = None) -> bool:
        if target_field_conditions is None:
            target_field_conditions = self.target_field_conditions

        if 0 <= x <= 7 and 0 <= y <= 7:
            position = (x, y)
            target_field = board[y][x]
            for condition in target_field_conditions:
                if target_field == condition:
                    positions.append(position)
                    return True
        return False

    def generate_possible_positions(self, current_position: Position, board: BoardArray) -> Positions:
        possible_positions = []
        for move_groups in self.possible_move_groups:
            for move in move_groups:
                x = current_position[0] + move[0]
                y = current_position[1] + move[1]
                if not self.check_if_position_is_legal(board, possible_positions, x, y):
                    break
                if board[y][x] == (not self.is_white) and board[y][x] != 'EmptyField':
                    break
        return possible_positions

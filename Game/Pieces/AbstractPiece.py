import abc


class AbstractPiece(abc.ABC):
    position = (0, 0)
    positions = []

    def __init__(self, is_white):
        self.is_white = is_white
        if self.is_white:
            self.short = self.short.upper()
            self.direction_multiplier = 1
        else:
            self.value = self.value * -1
            self.direction_multiplier = -1

        self.moved = False
        self.target_field_conditions = [
            not self.is_white,
            'EmptyField'
        ]

    def check_if_position_is_legal(self, board, positions, x, y, target_field_conditions=False):
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
    def filter_positions(positions):
        return list(filter(lambda position: 0 <= position[0] <= 7 and 0 <= position[1] <= 7, positions))

    @abc.abstractmethod
    def generate_possible_positions(self, current_position, board):
        pass

    @abc.abstractmethod
    def get_value(self):
        pass

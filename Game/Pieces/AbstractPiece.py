import abc


class AbstractPiece(abc.ABC):
    position = (0, 0)
    positions = []

    def __init__(self, is_white):
        self.isWhite = is_white
        if self.isWhite:
            self.short = self.short.upper()
            self.direction_multiplier = 1
        else:
            self.value = self.value * -1
            self.direction_multiplier = -1

    @abc.abstractmethod
    def generate_possible_positions(self, current_position, board):
        pass

    @abc.abstractmethod
    def get_value(self):
        pass

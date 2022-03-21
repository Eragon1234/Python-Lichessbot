from game.pieces.abstract_piece import AbstractPiece


class EmptyField(AbstractPiece):
    is_white = "EmptyField"
    short = 'e'
    lower_short = 'e'
    value = 0

    def __init__(self):
        # TODO: implements super().__init__()
        pass

    def generate_possible_positions(self, current_position, board):
        return []

    def get_value(self):
        return self.value

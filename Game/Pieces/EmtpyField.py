class EmptyField:
    isWhite = "EmptyField"
    short = 'e'
    value = 0

    def __init__(self):
        pass

    def generate_possible_positions(self, currentPosition, board):
        return []

    def get_value(self, position=False):
        return self.value

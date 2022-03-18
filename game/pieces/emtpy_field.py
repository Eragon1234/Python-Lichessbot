import os
import sys

sys.path.append(os.getcwd())

from game.pieces.abstract_piece import AbstractPiece


class EmptyField(AbstractPiece):
    is_white = "EmptyField"
    short = 'e'
    value = 0

    def __init__(self):
        pass

    def generate_possible_positions(self, current_position, board):
        return []

    def get_value(self, position=False):
        return self.value

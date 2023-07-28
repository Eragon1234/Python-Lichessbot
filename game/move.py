from typing import NamedTuple

from game.coordinate import Coordinate


class Move(NamedTuple):
    start_field: Coordinate
    target_field: Coordinate

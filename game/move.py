from typing import NamedTuple

from game.coordinate import Coordinate


class Move(NamedTuple):
    start_field: Coordinate
    target_field: Coordinate

    @classmethod
    def from_uci(cls, uci: str):
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:])
        return cls(start_field, target_field)

    def uci(self):
        return f"{self.start_field.uci()}{self.target_field.uci()}"

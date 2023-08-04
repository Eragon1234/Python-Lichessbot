from typing import NamedTuple

from game.coordinate import Coordinate


class Move(NamedTuple):
    start_field: Coordinate
    target_field: Coordinate

    @classmethod
    def from_uci(cls, uci: str):
        """
        Converts a UCI string to a Move object.

        Args:
            uci: The UCI string representing the move.

        Returns:
            Move: A Move object representing the move.

        Raises:
            ValueError: If the UCI string is not 4 characters long.
        """
        if len(uci) != 4:
            raise ValueError(f"UCI must be 4 characters long, not {len(uci)}")
        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:])
        return cls(start_field, target_field)

    def uci(self):
        return f"{self.start_field.uci()}{self.target_field.uci()}"

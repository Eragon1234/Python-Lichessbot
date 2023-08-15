from dataclasses import dataclass
from typing import Optional

from game.coordinate import Coordinate
from game.piece import PieceType


@dataclass
class Move:
    start_field: Coordinate
    target_field: Coordinate

    promote_to: Optional[PieceType] = None

    @classmethod
    def from_uci(cls, uci: str):
        """
        Converts a UCI string to a Move object.

        Args:
            uci: The UCI string representing the move.

        Returns:
            Move: A Move object representing the move.

        Raises:
            ValueError: If the UCI string is not 4 or 5 characters long.
        """
        if len(uci) != 4 and len(uci) != 5:
            raise ValueError(f"UCI must be 4 characters long, not {len(uci)}")

        start_field = Coordinate.from_uci(uci[:2])
        target_field = Coordinate.from_uci(uci[2:4])
        promote_to = uci[4] if len(uci) == 5 else None
        if promote_to is not None:
            promote_to = PieceType(promote_to)

        return cls(start_field, target_field, promote_to)

    def uci(self):
        promote = self.promote_to.value if self.promote_to is not None else ""
        return f"{self.start_field.uci()}{self.target_field.uci()}{promote}"

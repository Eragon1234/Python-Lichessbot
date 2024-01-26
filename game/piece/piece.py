from collections.abc import Iterator
from typing import Optional

from game.castling_rights import CastlingRights
from game.coordinate import Coordinate
from game.piece.board import Board
from game.piece.bonus import BONUS_MAPS
from game.piece.color import Color
from game.piece.move_factory import MoveFactory
from game.piece.move_groups import MOVE_GROUPS, FORWARD, LEFT, RIGHT
from game.piece.piece_type import PieceType
from game.piece.values import VALUES

PROMOTE_TYPES = [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP,
                 PieceType.KNIGHT]


class Piece[Move]:
    """
    A piece on a chess board.
    The type attribute specifies the type of the piece.
    The piece can also represent an empty field.
    """

    def __init__(self, move_factory: MoveFactory[Move],
                 piece_type: PieceType, color: Color):

        self.type = piece_type

        self.color = color

        self.value = VALUES[self.type]
        if self.color is Color.BLACK:
            self.value = -self.value

        self.legal_target_colors = self.color.enemy() | Color.EMPTY

        self.possible_move_groups = MOVE_GROUPS[self.type]

        self.bonus_map = BONUS_MAPS[self.type]

        self.move_factory = move_factory

    def moves(self, board: Board, pos: Coordinate,
              en_passant: Optional[Coordinate] = None,
              castling_rights: CastlingRights = CastlingRights.NONE) -> Iterator[Move]:
        """
        Generates possible moves for a piece on the given chess board.

        Args:
            board: The chess board.
            pos: The current position of the piece.
            en_passant: Optional en passant position.
            castling_rights: Optional castling rights.

        Returns:
            A generator object that yields possible moves for the piece.
        """
        if self.type is not PieceType.KING:
            yield from self._moves_with_move_groups(board, pos)

        if self.type is PieceType.PAWN:
            yield from self._moves_for_pawn(board, pos, en_passant)

        if self.type is PieceType.KING:
            yield from self._king_moves(board, pos, castling_rights)

    def _king_moves(self, board: Board, pos: Coordinate,
                    castling_rights: CastlingRights) -> Iterator[Move]:
        """
        Generates possible moves for a king on the given chess board.
        """
        for move in self._moves_with_move_groups(board, pos):
            yield self.move_factory.king_move(move.start_field,
                                              move.target_field)

        yield from self._castling_moves(board, pos, castling_rights)

    def _castling_moves(self, board: Board, pos: Coordinate,
                        castling_rights: CastlingRights) -> Iterator[Move]:
        """
        Generates possible castling moves for a king on the given chess board.
        """
        if castling_rights is CastlingRights.NONE:
            return

        castling: list[tuple[Coordinate, int]] = []
        king = pos
        if self.color is Color.WHITE:
            if CastlingRights.WHITE_KING in castling_rights:
                castling.append((Coordinate(7, 0), 1))
            if CastlingRights.WHITE_QUEEN in castling_rights:
                castling.append((Coordinate(0, 0), -1))
        else:
            if CastlingRights.BLACK_KING in castling_rights:
                castling.append((Coordinate(0, 7), -1))
            if CastlingRights.BLACK_QUEEN in castling_rights:
                castling.append((Coordinate(7, 7), 1))

        for rook, steps in castling:
            for x in range(king[0] + steps, rook[0], steps):
                if not board.is_type(Coordinate(x, king.y).value, PieceType.EMPTY):
                    break
            else:
                target = king[0] + 2 * steps
                yield self.move_factory.castle_move(king,
                                                    Coordinate(target, king[1]))

    def _moves_with_move_groups(self, board: Board,
                                pos: Coordinate) -> Iterator[Move]:
        """
        Generates possible moves for a piece on the given chess board.

        Args:
            board: The chess board.
            pos: The current position of the piece.

        Returns:
            A generator object that yields possible moves for the piece.
        """
        for move_group in self.possible_move_groups:
            for move in move_group:
                new_pos = pos + move
                target_field_color = board.color_at(new_pos)

                if target_field_color not in self.legal_target_colors:
                    break

                yield self.move_factory.from_type(self.type, pos, new_pos)

                if target_field_color is not Color.EMPTY:
                    break

    def _moves_for_pawn(self, board: Board, pos: Coordinate,
                        en_passant: Optional[Coordinate] = None) -> Iterator[Move]:
        """
        Generates possible moves for a pawn on the given chess board.

        Args:
            board: The chess board.
            pos: The current position of the pawn.
            en_passant: The position where a pawn could move en passant.

        Returns:
            A generator object that yields possible moves for the pawn.
        """
        promote = self.is_start_rank(pos, self.color.enemy())
        for target in self._positions_for_pawn(board, pos, en_passant):
            if not promote:
                yield self.move_factory.pawn_move(pos, target)
                continue

            for piece_type in PROMOTE_TYPES:
                yield self.move_factory.pawn_promotion(pos, target,
                                                       promote_to=piece_type)

    def _positions_for_pawn(self, board: Board, pos: Coordinate,
                            en_passant: Optional[Coordinate] = None) -> Iterator[Coordinate]:
        """
        Generates possible positions for a pawn on the given chess board.
        """
        forward = FORWARD
        if self.color is Color.BLACK:
            forward = -forward

        possible_target = pos + forward
        if board.is_type(possible_target.value, PieceType.EMPTY):
            yield possible_target

            if self.is_start_rank(pos):
                possible_target = pos + 2 * forward
                if board.is_type(possible_target.value, PieceType.EMPTY):
                    yield possible_target

        possible_target = pos + LEFT + forward
        target_field_color = board.color_at(possible_target)
        if target_field_color is self.color.enemy():
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

        possible_target = pos + RIGHT + forward
        target_field_color = board.color_at(possible_target)
        if target_field_color is self.color.enemy():
            yield possible_target

        if en_passant == possible_target:
            yield en_passant

    def is_start_rank(self, pos: Coordinate,
                      color: Optional[Color] = None) -> bool:
        """
        Checks if a given position is the start rank for a pawn of the color.

        Args:
            pos: The position to check.
            color: The color of the pawn. Defaults to the color of the piece.

        Returns:
            bool: whether the position is the start rank for a pawn.
        """
        if color is None:
            color = self.color
        start_rank = 1 if color is Color.WHITE else 6
        return pos[1] == start_rank

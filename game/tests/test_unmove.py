import unittest

import hypothesis.strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition

from game import ChessBoard


class BoardModel(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.board = ChessBoard()

    @precondition(lambda self: len(list(self.board.legal_moves())) > 0)
    @rule(
        data=st.data()
    )
    def move(self, data: st.SearchStrategy):
        move = data.draw(st.sampled_from(
            sorted(self.board.legal_moves(),
                   key=lambda m: m.uci())
        ))
        self.board.move(move)

    @precondition(lambda self: len(self.board.moves) > 0)
    @rule()
    def unmove(self):
        self.board.unmove()

    @rule()
    def correct_position(self):
        test_board = ChessBoard()
        for move in self.board.moves:
            test_board.move(move)

        assert self.board.fen() == test_board.fen()


TestUnmoveTestCase: unittest.TestCase = BoardModel.TestCase

"""
Test code for chess game
"""

import pytest
from chess import ChessStub
from board import Board

def test_init() -> None:
    """
    Tests that chess game initializes correctly
    """
    ChessStub()

def test_init_attribs() -> None:
    """
    Tests if chess game attributes initialize correctly
    """
    game = ChessStub()
    assert isinstance(game._board, Board)
    for i, rank in enumerate(game._board._board):
        for j, _ in enumerate(rank):
            assert game._board._board[i][j] is None
    assert game._turn == 0
    assert game._captured_pieces

def test_init_board_setup() -> None:
    """
    Tests if the board is set up correctly
    """
    game = ChessStub()
    game.restart()

    for i, rank in enumerate(game._board._board):
        for j, _ in enumerate(rank):
            assert game._board._board[i][j] is None
            raise NotImplementedError

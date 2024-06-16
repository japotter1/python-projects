"""
Internal game logic of the chess game
"""

from typing import Optional
from board import Position, Piece, Board


class ChessStub:
    """
    Stub implementation of chess game
    """

    _board: Board
    _turn: int
    _captured_pieces: dict[str, list[str]]

    piece_values: dict[str, int] = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 9,
                                    "K": 0}

    def __init__(self) -> None:
        """
        Constructor: creates a Board object, sets the turn to white, and sets
        up the board
        """
        self._board = Board()
        self._turn = 0
        self._captured_pieces = {"W": [], "B": []}

    @property
    def board(self) -> Board:
        """
        Returns the value of the _board attribute
        """
        return self._board

    @property
    def turn(self) -> int:
        """
        Returns the current turn as an int (0 for white, 1 for black)
        """
        return self._turn
    
    @property
    def game_over(self) -> bool:
        """
        Returns bool for whether the game is over or not
        """
        return False

    def restart(self) -> None:
        """
        Restarts the game in the starting position, white to move
        """
        self._board.set_up()
        self._turn = 0
        self._captured_pieces = {"W": [], "B": []}

    def next_turn(self) -> None:
        """
        Changes the turn to the other player
        """
        if self._turn == 0:
            self._turn = 1
        else:
            self._turn = 0

    def check_legal_move(self, pos1: Position, pos2: Position) -> bool:
        """
        Checks if a move can legally be made
        """
        raise NotImplementedError

    def play_move(self, pos1: Position, pos2: Position) -> None:
        """
        Plays a legal move
        """
        raise NotImplementedError

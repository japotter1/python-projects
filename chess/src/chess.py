"""
Internal game logic of the chess game
"""

import operator
from typing import Optional
from board import Position, Color, PieceType, Piece, Board


class ChessStub:
    """
    Stub implementation of chess game
    """

    _board: Board
    _turn: int
    _captured_pieces: dict[str, list[str]]

    _white_can_castle: bool
    _black_can_castle: bool

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

    def list_legal_moves(self, pos: Position) -> list[Position]:
        """
        Lists the squares that the piece at pos can legally move to (includes
        captures)
        """
        if not self.board.is_valid_position(pos):
            raise ValueError("Game Error: invalid position")
        
        piece = self.board.get_piece(pos)

        if piece is None:
            raise ValueError("Game Error: no piece to move from position")
        
        r, f = pos
        result = []

        # Pawn
        if piece.ptype == PieceType.P:
            op = operator.sub if piece.color == Color.W else operator.add
            start_rank = 6 if piece.color == Color.W else 1

            # Pawn moves
            if 0 < r < 7 and self.board.is_empty((op(r, 1), f)):
                result.append((op(r, 1), f))
                if r == start_rank and self.board.is_empty((op(r, 2), f)):
                    result.append((op(r, 2), f))
            
            # Pawn captures
            if 0 < r < 7:
                if f > 0 and not self.board.is_empty((op(r, 1), f-1)) and\
                self.board.get_piece((op(r, 1), f-1)).color != piece.color:
                    result.append((op(r, 1), f-1))
                if f < 7 and not self.board.is_empty((op(r, 1), f+1)) and\
                self.board.get_piece((op(r, 1), f+1)).color != piece.color:
                    result.append((op(r, 1), f+1))

        # Knight
        if piece.ptype == PieceType.N:
            for i, j in [(-2,-1), (-2,1), (-1,-2), (-1,2),
                         (1,-2), (1,2), (2,-1), (2,1)]:
                if self.board.is_valid_position((r+i, f+j)):
                    result.append((r+i, f+j))

        # Bishop or queen
        if piece.ptype == PieceType.B or piece.ptype == PieceType.Q:
            for direction in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                result.extend(self._long_moves(pos, direction))

        # Rook or queen
        if piece.ptype == PieceType.R or piece.ptype == PieceType.Q:
            for direction in [(-1,0), (0,-1), (0,1), (1,0)]:
                result.extend(self._long_moves(pos, direction))

        # King
        if piece.ptype == PieceType.K:
            for i, j in [(-1,-1), (-1,0), (-1,1), (0,-1),
                         (0,1), (1,-1), (1,0), (1,1)]:
                if self.board.is_valid_position((r+i, f+j)):
                    result.append((r+i), (f+j))

        return result

    def _long_moves(self, pos: Position, direction: Position) -> list[Position]:
        """
        Returns a list of all legal "long" moves (bishop/rook/queen) based on
        the given direction
        """
        raise NotImplementedError

    def _is_legal_move(self, pos1: Position, pos2: Position) -> bool:
        """
        Checks if the space exists, if it would cause check, etc
        To only be used inside list_legal_moves (this does not check if the
        piece can actually move there)
        """
        raise NotImplementedError

    def play_move(self, pos1: Position, pos2: Position) -> None:
        """
        Plays a legal move
        """
        raise NotImplementedError

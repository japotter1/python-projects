"""
Classes for chess pieces and board
"""

from typing import Optional
from enum import Enum

Position = tuple[int, int]

class Color(Enum):
    """
    Piece color
    """
    W = 0
    B = 1

class PieceType(Enum):
    """
    Piece type
    """
    P = 0
    N = 1
    B = 2
    R = 3
    Q = 4
    K = 5

class Piece:
    """
    Implementation of chess piece
    
    Attributes:
        _color: color of the piece
        _ptype: type of the piece
    """
    _color: Color
    _ptype: PieceType
    # _position: Position

    def __init__(self, color: Color, ptype: PieceType) -> None:
        """
        Creates piece object
        """
        self._color = color
        self._ptype = ptype

    @property
    def color(self) -> Color:
        return self._color

    @property
    def ptype(self) -> PieceType:
        return self._ptype

    def __str__(self) -> str:
        return f"{self.color.name}{self.ptype.name}"


class Board:
    """
    Implementation of chess board

    Attributes:
        _board: matrix representation of the board, storing Piece objects
    """
    _board: list[list[Optional[Piece]]]

    first_rank_setup: list[PieceType] = [PieceType.R, PieceType.N,
                                         PieceType.B, PieceType.Q,
                                         PieceType.K, PieceType.B,
                                         PieceType.N, PieceType.R]

    def __init__(self) -> None:
        """
        Constructor
        Creates an 8x8 game board
        """
        self._board = [[None] * 8 for _ in range(8)]
    
    def is_valid_position(self, pos: Position) -> bool:
        """
        Determines if the position is valid
        """
        r, f = pos
        return 0 <= r <= 7 and 0 <= f <= 7

    ### Modify board ###

    def add_piece(self, piece: Piece, pos: Position) -> None:
        """
        Puts a piece in the given position if it is empty
        Raises ValueError if it is not empty
        Raises ValueError if position is invalid
        """
        r, f = pos
        if not self.is_valid_position(pos):
            raise ValueError("Board Error: Invalid position")

        if self.is_empty(pos):
            self._board[r][f] = piece
        else:
            raise ValueError("Board Error: Position already occupied")

    def remove_piece(self, pos: Position) -> Optional[Piece]:
        """
        Removes the piece from the given position and returns its value
        Returns None if the position is empty
        Raises ValueError if position is invalid
        """
        r, f = pos
        if not self.is_valid_position(pos):
            raise ValueError("Board Error: Invalid position")

        removed_piece = self._board[r][f]
        self._board[r][f] = None

        return removed_piece

    def get_piece(self, pos: Position) -> Optional[Piece]:
        """
        Returns the value of the piece at the given position but does not
        remove it
        Returns None if the position is empty
        Raises ValueError if position is invalid
        """
        r, f = pos
        if not self.is_valid_position(pos):
            raise ValueError("Board Error: Invalid position")

        return self._board[r][f]

    def is_empty(self, pos: Position) -> bool:
        """
        Returns whether the position is empty
        Raises ValueError if position is invalid
        """
        r, f = pos
        if not self.is_valid_position(pos):
            raise ValueError("Board Error: Invalid position")

        return self._board[r][f] is None

    def move_piece(self, pos1: Position, pos2: Position) -> Optional[Piece]:
        """
        Removes the piece from the first position and adds it to the second
        If a piece was on the second, returns it
        Raises ValueError if both positions are the same or either position is
        invalid. Raises ValueError if original position is empty
        """
        if pos1 == pos2:
            raise ValueError("Board Error: Can't move to same square")

        moved_piece = self.remove_piece(pos1)
        if moved_piece is None:
            raise ValueError("Board Error: Can't move from empty square")

        captured_piece = self.remove_piece(pos2)
        self.add_piece(moved_piece, pos2)

        return captured_piece

    # def capture_piece(self, pos1: Position, pos2: Position) -> Piece:
    #     """
    #     Removes the piece from the second position and moves the piece from
    #     the first position to the second. Returns the captured piece.

    #     Raises ValueError if either position is empty or both positions are
    #     the same
    #     Raises ValueError if position is invalid (within called methods)
    #     """
    #     if self.is_empty(pos1) or self.is_empty(pos2):
    #         raise ValueError("Board Error: Invalid Capture")
    #     if pos1 == pos2:
    #         raise ValueError("Board Error: Can't capture on same square")

    #     captured_piece = self.remove_piece(pos2)
    #     self.move_piece(pos1, pos2)

    #     return captured_piece
        
    def clear(self) -> None:
        """
        Removes all pieces on the board
        """
        for i, rank in enumerate(self._board):
            for j, _ in enumerate(rank):
                self._board[i][j] = None

    def set_up(self) -> None:
        """
        Sets the board to the starting position
        """
        self.clear()

        for i in range(8):
            self.add_piece(Piece(Color.B, self.first_rank_setup[i]), (0, i))
            self.add_piece(Piece(Color.B, PieceType.P), (1, i))
            self.add_piece(Piece(Color.W, PieceType.P), (6, i))
            self.add_piece(Piece(Color.W, self.first_rank_setup[i]), (7, i))

    def __str__(self) -> str:
        """
        String representation of board for tui
        """
        result = "  a  b  c  d  e  f  g  h "
        for i, r in enumerate(self._board):
            result += f"\n{8-i}"
            for piece in r:
                if piece is None:
                    result += " --"
                else:
                    result += " " + str(piece)
        
        return result

"""
Classes for chess pieces and board
"""

from typing import Optional

Position = tuple[int, int]


class Piece:
    """
    Implementation of chess piece
    
    Attributes:
        _color: color of the piece
        _ptype: type of the piece
    """
    _color: str
    _ptype: str

    def __init__(self, color: str, ptype: str) -> None:
        """
        Creates piece object
        Raises ValueError if color or ptype is invalid
        """
        if color not in {"W", "B"} or\
            ptype not in {"P", "N", "B", "R", "Q", "K"}:
            raise ValueError("Invalid Color or Piece Type")

        self._color = color
        self._ptype = ptype

    @property
    def color(self):
        return self._color

    @property
    def ptype(self):
        return self._ptype

    def __str__(self) -> str:
        return f"{self.color}{self.ptype}"


class Board:
    """
    Implementation of chess board

    Attributes:
        _board: matrix representation of the board, storing Piece objects

    Note: Positions are indicated by Position type, a (rank, file) tuple
    """

    _board: list[list[Optional[Piece]]]

    first_rank_setup: list[str] = ["R", "N", "B", "Q", "K", "B", "N", "R"]

    def __init__(self) -> None:
        """
        Constructor
        Creates an 8x8 game board
        """
        self._board = [[None] * 8 for _ in range(8)]

    def add_piece(self, piece: Piece, pos: Position) -> None:
        """
        Puts a piece in the given position if it is empty
        Raises ValueError if it is not empty
        """
        r, f = pos

        if self.get_piece(pos) is None:
            self._board[r][f] = piece
        else:
            raise ValueError("Position already occupied")

    def remove_piece(self, pos: Position) -> Optional[Piece]:
        """
        Removes the piece from the given position and returns its value
        """
        r, f = pos

        removed_piece = self._board[r][f]
        self._board[r][f] = None

        return removed_piece

    def get_piece(self, pos: Position) -> Optional[Piece]:
        """
        Returns the value of the piece at the given position but does not
        remove it
        """
        r, f = pos
        return self._board[r][f]

    def move_piece(self, pos1: Position, pos2: Position) -> None:
        """
        Removes the piece from the first position and adds it to the second

        Raises ValueError if pos1 is empty or if pos2 is not empty
        """
        if self.get_piece(pos1) is None or self.get_piece(pos2) is not None:
            raise ValueError("Invalid move")

        moved_piece = self.remove_piece(pos1)
        self.add_piece(moved_piece, pos2)

    def capture_piece(self, pos1: Position, pos2: Position) -> Piece:
        """
        Removes the piece from the second position and moves the piece from
        the first position to the second. Returns the captured piece.

        Raises ValueError if either position is empty
        """
        if self.get_piece(pos1) is None or self.get_piece(pos2) is None:
            raise ValueError("Invalid Move")

        captured_piece = self.remove_piece(pos2)
        self.move_piece(pos1, pos2)

        return captured_piece
        
    def clear_board(self) -> None:
        """
        Removes all pieces on the board
        """
        for i, rank in enumerate(self._board):
            for j, _ in enumerate(rank):
                self._board[i][j] = None

    def set_up(self, clear: bool = True) -> None:
        """
        Sets the board to the starting position
        Clears the board first if clear is set to true (default)
        """
        if clear:
            self.clear_board()

        for i in range(8):
            self._board[0][i] = Piece("B", self.first_rank_setup[i])
            self._board[1][i] = Piece("B", "P")
            self._board[6][i] = Piece("W", "P")
            self._board[7][i] = Piece("W", self.first_rank_setup[i])

    def __str__(self) -> str:
        """
        String representation of board for debugging
        """
        result = ""
        for r in self._board:
            result += "\n"
            for piece in r:
                if piece is None:
                    result += " --"
                else:
                    result += " " + str(piece)
        
        return result

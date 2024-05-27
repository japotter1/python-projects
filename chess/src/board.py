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
    
    ### Move types ###

    def white_pawn_moves(self) -> list[Position]:
        """
        Returns the relative positions that a white pawn could move to from 0,0
        """
        result = []
        result.append((-1, 0))
        result.append((-2, 0))
        return result

    def white_pawn_captures(self) -> list[Position]:
        """
        Returns the relative positions that a white pawn could capture
        """
        result = []
        result.append((-1, -1))
        result.append((-1, 1))
        return result
    
    def black_pawn_moves(self) -> list[Position]:
        """
        Returns the relative positions that a black pawn could move to from 0,0
        """
        result = []
        result.append((1, 0))
        result.append((2, 0))
        return result

    def black_pawn_captures(self) -> list[Position]:
        """
        Returns the relative positions that a black pawn could capture
        """
        result = []
        result.append((1, -1))
        result.append((1, 1))
        return result
    
    def knight_moves(self) -> list[Position]:
        """
        Returns the relative positions that a knight could move to/capture
        """
        result = []
        for i in [-2, -1, 1, 2]:
            result.append((i, 3-abs(i)))
            result.append((i, -(3-abs(i))))
        return result
    
    def king_moves(self) -> list[Position]:
        """
        Returns the relative positions that a knight could move to/capture
        """
        result = []
        for i in range(-1,2):
            for j in range(-1,2):
                # if not i == 0 and j == 0:
                    result.append((i,j))
        return result

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

    ### String converters ###

    def str_to_pos(self, pos: str) -> Position:
        """
        Converts the name of a square (eg. A1) to position tuple (eg. (0,7))
        Raises ValueError if position is invalid
        """
        rank: int = 8 - int(pos[1])
        file: int = ord(pos[0]) - 65

        if not self.is_valid_position((rank, file)):
            raise ValueError("Invalid position")

        return rank, file
        
    def str_to_piece(self, piece: str) -> Piece:
        """
        Converts the name of a piece (eg. BK) to Piece object (a black king)
        Raises ValueError if piece name is invalid
        """
        try:
            color: Color = Color[piece[0]]
            ptype: PieceType = PieceType[piece[1]]
        except KeyError:
            raise ValueError("Invalid piece color or type")

        return Piece(color, ptype)

    ### Modify board ###

    def add_piece(self, piece: Piece, pos: Position) -> None:
        """
        Puts a piece in the given position if it is empty
        Raises ValueError if it is not empty
        Raises ValueError if position is invalid
        """
        r, f = pos
        if not self.is_valid_position(pos):
            raise ValueError("Invalid position")

        if self.get_piece(pos) is None:
            self._board[r][f] = piece
        else:
            raise ValueError("Position already occupied")

    def remove_piece(self, pos: Position) -> Optional[Piece]:
        """
        Removes the piece from the given position and returns its value
        Raises ValueError if position is invalid
        """
        r, f = pos
        if not self.is_valid_position(pos):
            raise ValueError("Invalid position")

        removed_piece = self._board[r][f]
        self._board[r][f] = None

        return removed_piece

    def get_piece(self, pos: Position) -> Optional[Piece]:
        """
        Returns the value of the piece at the given position but does not
        remove it
        Raises ValueError if position is invalid
        """
        r, f = pos
        if not self.is_valid_position(pos):
            raise ValueError("Invalid position")

        return self._board[r][f]

    def move_piece(self, pos1: Position, pos2: Position) -> None:
        """
        Removes the piece from the first position and adds it to the second

        Raises ValueError if pos1 is empty or if pos2 is not empty or both
        positions are the same
        Raises ValueError if position is invalid (within called methods)
        """
        if self.get_piece(pos1) is None or self.get_piece(pos2) is not None:
            raise ValueError("Invalid move")
        if pos1 == pos2:
            raise ValueError("Can't move to same square")

        moved_piece = self.remove_piece(pos1)
        self.add_piece(moved_piece, pos2)

    def capture_piece(self, pos1: Position, pos2: Position) -> Piece:
        """
        Removes the piece from the second position and moves the piece from
        the first position to the second. Returns the captured piece.

        Raises ValueError if either position is empty or both positions are
        the same
        Raises ValueError if position is invalid (within called methods)
        """
        if self.get_piece(pos1) is None or self.get_piece(pos2) is None:
            raise ValueError("Invalid Move")
        if pos1 == pos2:
            raise ValueError("Can't capture on same square")

        captured_piece = self.remove_piece(pos2)
        self.move_piece(pos1, pos2)

        return captured_piece
    
    ### Movement Methods ###

    def moveset(self, pos: Position) -> set[Position]:
        """
        Returns the set of positions that the piece at the given position could
        move to
        
        Raises ValueError if the starting position is invalid (within called
        methods)
        """
        r, f = pos
        piece = self.get_piece(pos)

        result = set()

        if piece is None:
            return result

        assert isinstance(piece, PieceType)

        if piece.ptype == PieceType.P:
            pass
        if piece.ptype == PieceType.N:
            pass
        if piece.ptype == PieceType.B:
            pass
        if piece.ptype == PieceType.R:
            pass
        if piece.ptype == PieceType.Q:
            pass
        if piece.ptype == PieceType.K:
            pass

    ### Setup/Clear ###
        
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

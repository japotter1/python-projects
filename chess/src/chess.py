"""
Internal game logic of the chess game
"""

import numpy
import operator
from copy import deepcopy
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
    
    first_rank_setup: list[PieceType] = [PieceType.R, PieceType.N,
                                         PieceType.B, PieceType.Q,
                                         PieceType.K, PieceType.B,
                                         PieceType.N, PieceType.R]

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
    def is_in_check(self) -> bool:
        """
        Returns whether the current player is in check or not
        """
        for pos, piece in self.board.pieces_on_board.items():
            if piece.color.value != self.turn:
                moves = self.list_legal_moves(pos, simulated=True)
                for move in moves:
                    target = self.board.get_piece(move)
                    if target is not None and target.ptype == PieceType.K:
                        return True

        return False
    
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
        self.board.clear()

        for i in range(8):
            self.board.add_piece(Piece(Color.B, self.first_rank_setup[i]), (0, i))
            self.board.add_piece(Piece(Color.B, PieceType.P), (1, i))
            self.board.add_piece(Piece(Color.W, PieceType.P), (6, i))
            self.board.add_piece(Piece(Color.W, self.first_rank_setup[i]), (7, i))

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

    def list_legal_moves(self, pos: Position, simulated: bool = False) -> list[Position]:
        """
        Lists the squares that the piece at pos can legally move to (includes
        captures)

        simulated (default false) is set to true when this function is used
        within the _would_be_check method, as a check is still valid even if
        "capturing the king" would put the opponent in check as well
        """
        if not self.board.is_valid_position(pos):
            raise ValueError("Game Error: invalid position")
        
        piece = self.board.get_piece(pos)

        r, f = pos
        result = []

        if piece is None:
            return result
        
        assert isinstance(piece, Piece)
        if not simulated and piece.color.value != self.turn:
            return result

        # Pawn
        if piece.ptype == PieceType.P:
            op = operator.sub if piece.color == Color.W else operator.add
            start_rank = 6 if piece.color == Color.W else 1

            # Pawn moves
            single_move = (op(r, 1), f)
            if self.board.is_valid_position(single_move) and\
                self.board.is_empty(single_move):
                result.append(single_move)
                
                double_move = (op(r, 2), f)
                if r == start_rank and\
                self.board.is_valid_position(double_move) and\
                self.board.is_empty(double_move):
                    result.append(double_move)

            # Pawn captures
            for i in [-1, 1]:
                capture = (op(r, 1), f+i)
                if self.board.is_valid_position(capture) and\
                isinstance(self.board.get_piece(capture), Piece) and\
                self.board.get_piece(capture).color != piece.color:
                    result.append(capture)

        # Knight
        elif piece.ptype == PieceType.N:
            for i, j in [(-2,-1), (-2,1), (-1,-2), (-1,2),
                         (1,-2), (1,2), (2,-1), (2,1)]:
                move = ((r+i, f+j))
                if self.board.is_valid_position(move):
                    if isinstance(self.board.get_piece(move), Piece) and\
                    self.board.get_piece(move).color == piece.color:
                        continue
                    result.append(move)

        # Bishop
        elif piece.ptype == PieceType.B:
            for direction in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                result.extend(self._long_moves(pos, direction))

        # Rook
        elif piece.ptype == PieceType.R:
            for direction in [(-1,0), (0,-1), (0,1), (1,0)]:
                result.extend(self._long_moves(pos, direction))

        # Queen
        elif piece.ptype == PieceType.Q:
            for direction in [(-1,-1), (-1,1), (1,-1), (1,1),
                              (-1,0), (0,-1), (0,1), (1,0)]:
                result.extend(self._long_moves(pos, direction))

        # King
        elif piece.ptype == PieceType.K:
            for i, j in [(-1,-1), (-1,0), (-1,1), (0,-1),
                         (0,1), (1,-1), (1,0), (1,1)]:
                move = ((r+i, f+j))
                if self.board.is_valid_position(move):
                    if isinstance(self.board.get_piece(move), Piece) and\
                    self.board.get_piece(move).color == piece.color:
                        continue
                    result.append(move)

        if simulated:
            return result
        
        return [move for move in result if not self._would_be_check(pos, move)]

    def _long_moves(self, pos: Position, direction: Position) -> list[Position]:
        """
        Returns a list of all legal "long" moves (bishop/rook/queen) based on
        the given direction
        """
        r, f = pos
        i, j = direction

        if i == 0 and j == 0:
            raise ValueError("Game Error: long move direction can't be (0,0)")

        if isinstance(self.board.get_piece(pos), Piece):
            color = self.board.get_piece(pos).color
        else:
            raise ValueError("Game Error: can't find long moves from empty position")

        result = []

        legal = True

        while legal:
            move = (r+i, f+j)
            if self.board.is_valid_position(move):
                if isinstance(self.board.get_piece(move), Piece):
                    if self.board.get_piece(move).color == color:
                        legal = False
                    else:
                        result.append(move)
                        legal = False
                else:
                    result.append(move)
                    i += numpy.sign(i)
                    j += numpy.sign(j)
            else:
                legal = False

        return result
    
    def _would_be_check(self, pos1: Position, pos2: Position) -> bool:
        """
        Simulates a move to determine it would put that player in check
        """
        game_copy: ChessStub = deepcopy(self)
        game_copy.play_move(pos1, pos2)
        game_copy.next_turn()

        return game_copy.is_in_check

    def play_move(self, pos1: Position, pos2: Position) -> None:
        """
        Plays a move. Does not check for legality. Increments the turn counter.
        """
        self.board.move_piece(pos1, pos2)
        self.next_turn()
    
    ### Notation ###

    ### String converters ###

    def str_to_pos(self, pos: str) -> Position:
        """
        Converts the name of a square (eg. A1) to position tuple (eg. (0,7))
        Raises ValueError if position is invalid
        """
        r: int = 8 - int(pos[1])
        f: int = ord(pos[0]) - 97

        if not 0 <= r <= 7 or not 0 <= f <= 7:
            raise ValueError("Invalid position")

        return r, f

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

    def read_notation(self, notation: str) -> tuple[Position, Position]:
        """
        Reads a string of notation and returns the tuple of start and end
        positions for the move

        NOTE to self: go backwards - start with last two
            if last two look like position, that's the end pos
            otherwise keep going back until you find it

            if there's nothing before those two it's a pawn move, check if legal

            if there's a capital letter at the start that's the piece. Otherwise it's a pawn move
                check if there's a piece of that type (of the current player's) that can legally move there
                if multiple, check after first letter for disambiguators
            if it starts with a lowercase letter, it's a pawn capture, check if legal
            """
        raise NotImplementedError
"""
Script for reading and writing chess notation
"""

from board import Position
from chess import ChessStub

def read_pgn(path: str):
    """
    pgn specifications: http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm
    """
    try:
        with open(path) as f:
            notation = f.read()

    except FileNotFoundError:
        return None

def read_move(notation: str, game: ChessStub) -> tuple[Position, Position]:
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
    stripped = notation.strip(" !?+-/=")

def write_move():
    raise NotImplementedError

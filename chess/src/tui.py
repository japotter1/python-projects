"""
Text user interface for chess game
"""

import sys
from typing import Optional
from chess import ChessStub
from board import Position

game = ChessStub()
game.restart()

def print_board(game: ChessStub, list_legal_pos: Optional[Position] = None) -> None:
    """
    Prints the game board
    """
    legal_marks = []
    if list_legal_pos is not None:
        legal_marks.extend(game.list_legal_moves(list_legal_pos))

    result = "   a   b   c   d   e   f   g   h  "
    for i in range(8):
        result += f"\n{8-i} "
        for j in range(8):
            piece = game.board.get_piece((i,j))
            if (i,j) in legal_marks:
                if piece is None:
                    result += "[--]"
                else:
                    result += "[" + str(piece) + "]"
            else:
                if piece is None:
                    result += " -- "
                else:
                    result += " " + str(piece) + " "
    
    print(f"\n{result}")

mark = None

while not game.game_over:
    print_board(game, mark)
    mark = None
    print("White to move") if game.turn == 0 else print("Black to move")
    if game.is_in_check:
        print("You are in check")

    move = input("\nPlease enter a move: ")

    if move == "exit":
        exit()

    try:
        if move.find("list ") == 0:
            print("\nLegal moves list:")
            legal_moves = game.list_legal_moves(game.str_to_pos(move[5:7]))
            for r, f in legal_moves:
                print(f"{chr(f+97)}{8-r}")
        elif move.find("mark ") == 0:
            mark = game.str_to_pos(move[5:7])
        else:
            game.play_move(game.str_to_pos(move[0:2]), game.str_to_pos(move[2:4]))
    except Exception as error:
        print(f"\nInvalid move: {error}")

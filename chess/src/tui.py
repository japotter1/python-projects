"""
Text user interface for chess game
"""

import sys
from chess import ChessStub
from board import str_to_piece, str_to_pos, is_valid_position

game = ChessStub()
game.restart()

while not game.game_over:
    print(game.board)
    print("White to move") if game.turn == 0 else print("Black to move")
    move = input("Please enter a move: ")

    if move == "exit":
        exit()

    try:
        game.board.move_piece(str_to_pos(move[0:2]), str_to_pos(move[2:4]))
    except ValueError:
        print("Invalid move")

    game.next_turn()
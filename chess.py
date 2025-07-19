import pygame
import numpy as np
import copy
import random
import math
from chess_utils import (Piece, board_setup, rook_moves, black_pawn_moves, tiles, init_board, action, 
     step, queen_direction, num_squares, square_occupied, queen_plane, plane, legal_moves, check, step, 
     turn_array, get_rook_castle, white_kingside_castle, black_kingside_castle, white_queenside_castle, 
     black_queenside_castle, moved_pieces, piece_group, only_legal_moves, game_end , update_board, value, make_move, best_move)

%load_ext autoreload
%reload_ext autoreload
%autoreload 2

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
running = True

board_image = pygame.image.load("chess_images/chessboard.png")
board_image = pygame.transform.scale(board_image, (720, 720))

board_state = init_board()
pieces = piece_group(board_state)
turn_color = 1
castle_moved = [0,0,0,0,0,0]
fifty_move_counter = 0

while running:

    board = tiles()
    colors = [1,0]
    turn_color = board_state[12][0][0]
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        # if mouse down on a piece, change the piece attribute to selected so it may be moved
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for piece in pieces:
                if piece.color == turn_color:
                    if piece.rect.collidepoint(pygame.mouse.get_pos()):
                        piece.selected = True
                        for k in range(64):
                            if board[k].collidepoint(piece.rect.center):
                                index = k
                        old_rect = board[index]
                        type = piece.type
                    
        # if mouse button down, unselect the piece and snap it to the square it was closest to
        elif event.type == pygame.MOUSEBUTTONUP:
            for piece in pieces:
                if piece.selected == True:

                    if turn_color == 1:
                        board_state[18] = [[0,0,0,0,0,0,0,0]]
                    if turn_color == 0:
                        board_state[19] = [[0,0,0,0,0,0,0,0]]
                    
                    piece.selected = False
                    index = 0
                    for k in range(64):
                        if board[k].collidepoint(piece.rect.center):
                            index = k
                    new_rect = board[index]

                    try:
                        board_state[18] = [[0,0,0,0,0,0,0,0]]
                        board_state = update_board(action(old_rect, new_rect), board_state)
                        pieces = piece_group(board_state)
                    except IndexError:
                        piece.rect = old_rect

                    if game_end(board_state) in [-1,0,1]:
                        running = False

                    screen.blit(board_image, (0,0))
                    for piece in pieces:
                        screen.blit(piece.image, piece.rect)
                    pygame.display.flip()

                    if board_state[12][0][0] == 0:

                        board_state[19] = [[0,0,0,0,0,0,0,0]]
                        scores = best_move(board_state)
                        act = random.choice(only_legal_moves(board_state)[np.where(np.array(scores) == max(scores))[0]])
                        board_state = update_board(act, board_state)
                        pieces = piece_group(board_state)

                        if game_end(board_state) in [-1,0,1]:
                            running = False
                            
        # if the mouse is being dragged while a piece is selected move the piece with the mouse
        elif event.type == pygame.MOUSEMOTION:
            for piece in pieces:
                if piece.selected:
                    piece.rect.center = pygame.mouse.get_pos()

    screen.blit(board_image, (0,0))
    for piece in pieces:
        screen.blit(piece.image, piece.rect)
    pygame.display.flip()  

pygame.quit()
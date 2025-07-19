import pygame
import copy
import numpy as np


def square_occupied(x,y,board_state):
    occ = 0
    type = 0
    if x < 0 or x > 7 or y < 0 or y > 7:
        occ = 2
        type = -1
    else:
        for i in range(12):
            if board_state[i][y][x] == 1:
                occ = 1
                type = i
    return occ, type


def queen_plane(direction, squares):
    n = 0
    p = 0
    for dir in range(8):
        for space in range(1,8):
            if direction == dir and space == squares:
                p = n
            else:
                n += 1
    return p

def check(board_state):
    turn_color = board_state[12][0][0]
    check = 0
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    delta_x_knight = [1,2,2,1,-1,-2,-2,-1]
    delta_y_knight = [-2,-1,1,2,2,1,-1,-2]
    x_king = np.where(np.array(board_state[[11,5][turn_color]]) == 1)[1][0]
    y_king = np.where(np.array(board_state[[11,5][turn_color]]) == 1)[0][0]
    for i in range(8):
        occupied, type = square_occupied(x_king + delta_x_knight[i], y_king + delta_y_knight[i], board_state)
        if turn_color == 1:
            if type == 7:
                check = 1
        elif turn_color == 0:
            if type == 1:
                check = 1
    for dir in range(8):
        x = x_king
        y = y_king
        occupied, type = square_occupied(x + delta_x[dir], y + delta_y[dir], board_state)
        steps = 0
        while occupied == 0:
            x = x + delta_x[dir]
            y = y + delta_y[dir]
            occupied, type = square_occupied(x + delta_x[dir], y + delta_y[dir], board_state)
            steps += 1
        if turn_color == 1:
            if type == -1:
                pass
            else:
                if dir == 0 or dir == 2 or dir == 4 or dir == 6:
                    if type == 11:
                        if steps == 0:
                            check = 1
                    elif type == 9 or type == 10:
                        check == 1
                elif dir == 1 or dir == 7:
                    if type == 6 or type == 11:
                        if steps == 0:
                            check = 1
                    elif type == 8 or type == 10:
                        check = 1
                elif dir == 3 or dir == 5:
                    if type == 11:
                        if steps == 0:
                            check = 1
                    elif type == 8 or type == 10:
                        check = 1
                    elif type == 6:
                        if steps == 0:
                            check = 1
        elif turn_color == 0:
            if type == -1:
                pass
            else:
                if dir == 0 or dir == 2 or dir == 4 or dir == 6:
                    if type == 5:
                        if steps == 0:
                            check = 1
                    elif type == 3 or type == 4:
                        check = 1
                elif dir == 1 or dir == 7:
                    if type == 0 or type == 5:
                        if steps == 0:
                            check = 1
                    elif type == 2 or type == 4:
                        check = 1
                elif dir == 3 or dir == 5:
                    if type == 5:
                        if steps == 0:
                            check = 1
                    elif type == 2 or type == 4:
                        check = 1
                    elif type == 0:
                        if steps == 0:
                            check = 1
    
    return check


def step(x,y,delta_x,delta_y,board_state):
    
    turn_color = board_state[12][0][0]
    move = 1
    capture = 0
    
    if turn_color == 1:
        if square_occupied(x, y, board_state)[1] > 5:
            move = 0
        if x + delta_x < 0:
            move = 0
        if x + delta_x > 7:
            move = 0
        if y + delta_y < 0:
            move = 0
        if y + delta_y > 7:
            move = 0
        if square_occupied(x + delta_x, y + delta_y, board_state)[0] == 1:
            if square_occupied(x + delta_x, y + delta_y, board_state)[1] > 5:
                move = 1
                capture = 1
            else:
                move = 0
                    
    if turn_color == 0:
        if square_occupied(x, y, board_state)[1] < 6:
            move = 0
        if x + delta_x < 0:
            move = 0
        if x + delta_x > 7:
            move = 0
        if y + delta_y < 0:
            move = 0
        if y + delta_y > 7:
            move = 0
        if square_occupied(x + delta_x, y + delta_y, board_state)[0] == 1:
            if square_occupied(x + delta_x, y + delta_y, board_state)[1] < 6:
                move = 1
                capture = 1
            else:
                move = 0

    if move == 1:
        board = copy.deepcopy(board_state)
        type = square_occupied(x,y,board)[1]
        board[type][y][x] = 0
        board[type][y + delta_y][x + delta_x] = 1
        if turn_color == 1:
            if square_occupied(x + delta_x, y + delta_y, board)[1] > 5:
                board[square_occupied(x + delta_x, y + delta_y, board)[1]][y + delta_y][x + delta_x] = 0
        if turn_color == 0:
            if square_occupied(x + delta_x, y + delta_y, board)[1] < 6:
                board[square_occupied(x + delta_x, y + delta_y, board)[1]][y + delta_y][x + delta_x] = 0
        if check(board) == 1:
            move = -1
    
    return move, capture

def game_end(board_state):
    in_check = check(board_state)
    num_moves = len(np.where(np.array(legal_moves(board_state)))[0])
    val = 2
    if board_state[12][0][0] == 1:
        if in_check:
            if num_moves == 0:
                val = -1
        else:
            if num_moves == 0:
                val = 0
            else:
                val = 2
    else:
        if in_check:
            if num_moves == 0:
                val = 1
        else:
            if num_moves == 0:
                val = 0
    if board_state[17][0][0] > 49:
        val = 0
    return val


def legal_moves(board_state):
    
    turn_color = board_state[12][0][0]
    legal_moves = [0 for i in range(4100)]
        
    for x in range(8):
        for y in range(8):
            type = square_occupied(x,y,board_state)[1]
            if square_occupied(x,y,board_state)[0]:
                if turn_color == 1:
                    if type == 0:
                        for action in white_pawn_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 1:
                        for action in knight_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 2:
                        for action in bishop_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 3:
                        for action in rook_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 4:
                        for action in queen_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 5:
                        for action in king_moves(x,y,board_state):
                            legal_moves[action] = 1
                elif turn_color == 0:
                    if type == 6:
                        for action in black_pawn_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 7:
                        for action in knight_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 8:
                        for action in bishop_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 9:
                        for action in rook_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 10:
                        for action in queen_moves(x,y,board_state):
                            legal_moves[action] = 1
                    elif type == 11:
                        for action in king_moves(x,y,board_state):
                            legal_moves[action] = 1
            else:
                pass

    if board_state[13][0][0] == 1:
        legal_moves[2511] = 1
    if board_state[14][0][0] == 1:
        legal_moves[2539] = 1
    if board_state[15][0][0] == 1:
        legal_moves[2063] = 1
    if board_state[16][0][0] == 1:
        legal_moves[2091] = 1
    
    return legal_moves

def plane(old_rect, new_rect):
    direc = queen_direction(old_rect, new_rect)
    num_spa = num_squares(old_rect, new_rect)
    n = 0
    p = 5000
    for dir in range(8):
        for space in range(1,8):
            if direc == dir and space == num_spa:
                p = n
            else:
                n += 1 
    if p > 55:
        delta_x = -int((old_rect[0] - new_rect[0]) / 90)
        delta_y = -int((old_rect[1] - new_rect[1]) / 90)
        if delta_x == 1 and delta_y == -2:
            p = 56
        elif delta_x == 2 and delta_y == -1:
            p = 57
        elif delta_x == 2 and delta_y == 1:
            p = 58
        elif delta_x == 1 and delta_y == 2:
            p = 59
        elif delta_x == -1 and delta_y == 2:
            p = 60
        elif delta_x == -2 and delta_y == 1:
            p = 61
        elif delta_x == -2 and delta_y == -1:
            p = 62
        elif delta_x == -1 and delta_y == -2:
            p = 63
        
    return p    


def knight_moves(x, y, board_state):
    legal_actions = []
    delta_x = [1,2,2,1,-1,-2,-2,-1]
    delta_y = [-2,-1,1,2,2,1,-1,-2]
    knight_plane = [56, 57, 58, 59, 60, 61, 62, 63]
    for i in range(8):
        if square_occupied(x,y,board_state)[0]:
            if step(x,y,delta_x[i],delta_y[i],board_state)[0] == 1:
                legal_actions.append(64 * (8*x + y) + knight_plane[i])
    return legal_actions


def king_moves(x, y, board_state):
    legal_actions = []
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    for i in range(8):
        if square_occupied(x,y,board_state)[0]:
            if step(x, y, delta_x[i], delta_y[i], board_state)[0] == 1:
                legal_actions.append(64 * (8*x + y) + queen_plane(i,1))
    return legal_actions

def white_pawn_moves(x,y,board_state):
    legal_actions = []
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    if square_occupied(x,y,board_state)[0]:
        if step(x,y,0,-1,board_state)[0] == 1:
            if step(x,y,0,-1,board_state)[1] == 0:
                legal_actions.append(64 * (8*x + y) + queen_plane(0,1))
    for i in [1,7]:
        if square_occupied(x,y,board_state)[0]:
            if step(x,y,delta_x[i],delta_y[i],board_state)[0] == 1:
                if step(x,y,delta_x[i],delta_y[i],board_state)[1] == 1:
                    legal_actions.append(64 * (8*x + y) + queen_plane(i,1))
                else:
                        if y == 3:
                            if i == 1:
                                if x + 1 < 8:
                                    if board_state[19][0][x + 1]:
                                        legal_actions.append(64 * (8*x + y) + queen_plane(i,1))
                            elif i == 7:
                                if x - 1 > -1:
                                    if board_state[19][0][x - 1]:
                                        legal_actions.append(64 * (8*x + y) + queen_plane(i,1))
    if y == 6:
        if square_occupied(x,y,board_state)[0]:
            if square_occupied(x,y-1,board_state)[0] == 0:
                if step(x,y,0,-2,board_state)[0] == 1:
                    if step(x,y,0,-2,board_state)[1] == 0:
                        legal_actions.append(64 * (8*x + y) + queen_plane(0,2))
    return legal_actions

def black_pawn_moves(x, y, board_state):
    legal_actions = []
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    if square_occupied(x,y,board_state)[0]:
        if step(x,y,0,1,board_state)[0] == 1:
            if step(x,y,0,1,board_state)[1] == 0:
                legal_actions.append(64 * (8*x + y) + queen_plane(4,1))
    for i in [3,5]:
        if square_occupied(x,y,board_state)[0]:
                if step(x,y,delta_x[i],delta_y[i],board_state)[0] == 1:
                    if step(x,y,delta_x[i],delta_y[i],board_state)[1] == 1:
                        legal_actions.append(64 * (8*x + y) + queen_plane(i,1))
                    else:
                        if y == 4:
                            if i == 3:
                                if x + 1 < 8:
                                    if board_state[18][0][x + 1]:
                                        legal_actions.append(64 * (8*x + y) + queen_plane(i,1))
                            elif i == 5:
                                if x - 1 > -1:
                                    if board_state[18][0][x - 1]:
                                        legal_actions.append(64 * (8*x + y) + queen_plane(i,1))
    if y == 1:
        if square_occupied(x,y,board_state)[0]:
            if square_occupied(x,y+1,board_state)[0] == 0:
                if step(x,y,0,2,board_state)[0] == 1:
                    if step(x,y,0,2,board_state)[1] == 0:
                        legal_actions.append(64 * (8*x + y) + queen_plane(4,2))
    
    return legal_actions

def queen_moves(x, y, board_state):
    legal_actions = []
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    for i in range(8):
        direction = i
        steps = 1
        if square_occupied(x,y,board_state)[0]:
            while step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == 1:
                legal_actions.append(64 * (8*x + y) + queen_plane(i,steps))
                if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[1] == 1:
                    break
                steps += 1
            if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == -1:
                for steps in [1,2,3,4,5,6,7]:
                    if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == 1:
                        legal_actions.append(64 * (8*x + y) + queen_plane(i,steps))
    return legal_actions

def rook_moves(x, y, board_state):
    legal_actions = []
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    for i in [0,2,4,6]:
        direction = i
        steps = 1
        if square_occupied(x,y,board_state)[0]:
            while step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == 1:
                legal_actions.append(64 * (8*x + y) + queen_plane(i,steps))
                if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[1] == 1:
                    break   
                steps += 1
            if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == -1:
                for steps in [1,2,3,4,5,6,7]:
                    if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == 1:
                        legal_actions.append(64 * (8*x + y) + queen_plane(i,steps))
    return legal_actions

def bishop_moves(x, y, board_state):
    legal_actions = []
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    for i in [1,3,5,7]:
        direction = i
        steps = 1
        if square_occupied(x,y,board_state)[0]:
            while step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == 1:
                legal_actions.append(64 * (8*x + y) + queen_plane(i,steps))
                if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[1] == 1:
                    break
                steps += 1
            if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == -1:
                for steps in [1,2,3,4,5,6,7]:
                    if step(x, y, steps * delta_x[i], steps * delta_y[i], board_state)[0] == 1:
                        legal_actions.append(64 * (8*x + y) + queen_plane(i,steps))
    return legal_actions


def queen_direction(old_rect, new_rect):
    x_old = old_rect[0]
    x_new = new_rect[0]
    y_old = old_rect[1]
    y_new = new_rect[1]
    if x_old == x_new:
        if y_old > y_new:
            return 0
        elif y_old < y_new:
            return 4
    elif x_old > x_new:
        if y_old == y_new:
            return 6
        elif y_old > y_new:
            return 7
        elif y_old < y_new:
            return 5
    elif x_old < x_new:
        if y_old == y_new:
            return 2
        elif y_old > y_new:
            return 1
        elif y_old < y_new:
            return 3

def num_squares(old_rect, new_rect):
    delta_x = int(abs(old_rect[0] - new_rect[0]) / 90)
    delta_y = int(abs(old_rect[1] - new_rect[1]) / 90)
    if delta_y == 0:
        return delta_x
    elif delta_x == 0:
        return delta_y
    else:
        if delta_x == delta_y:
            return delta_x
        else:
            return 9 
        
    return p


# dim(a) = 8*8*73 = 73*(56+7+1)
# a = x*y*p (from 1 to 8, p from 1 to 73) = 73(x*8+y)+p (from 0 to 7, p from 0 to 72)
# Then a // (8*73) = x, (a // 73) % 8 = y, and a % 73 = p
def action(old_rect, new_rect):
    x = old_rect[0] / 90
    y = old_rect[1] / 90
    a = 64 * ((8 * x) + y) + plane(old_rect, new_rect)
    return int(a)

class Piece(pygame.sprite.Sprite):
    
    def __init__(self, color, piece, x, y):

        pygame.sprite.Sprite.__init__(self)

        # Surface of the piece (image)

        if color == 1:
            
            self.color = 1
            
            if piece == 0:
                self.type = 0
                self.image = pygame.image.load("chess_images/pawn_white.png")
            elif piece == 1:
                self.type = 1
                self.image = pygame.image.load("chess_images/knight_white.png")
            elif piece == 2:
                self.type = 2
                self.image = pygame.image.load("chess_images/bishop_white.png")
            elif piece == 3:
                self.type = 3
                self.image = pygame.image.load("chess_images/rook_white.png")
            elif piece == 4:
                self.type = 4
                self.image = pygame.image.load("chess_images/queen_white.png")
            elif piece == 5:
                self.type = 5
                self.image = pygame.image.load("chess_images/king_white.png")

                
        elif color == 0:

            self.color = 0
            
            if piece == 6:
                self.type  = 6
                self.image = pygame.image.load("chess_images/pawn_black.png")
            elif piece == 7:
                self.type = 7
                self.image = pygame.image.load("chess_images/knight_black.png")
            elif piece == 8:
                self.type = 8
                self.image = pygame.image.load("chess_images/bishop_black.png")
            elif piece == 9:
                self.type = 9
                self.image = pygame.image.load("chess_images/rook_black.png")
            elif piece == 10:
                self.type = 10
                self.image = pygame.image.load("chess_images/queen_black.png")
            elif piece == 11:
                self.type = 11
                self.image = pygame.image.load("chess_images/king_black.png")
            
        self.image = pygame.transform.scale(self.image, (90, 90))
        
        # Position and dimensions of piece
        self.rect = pygame.Rect(x,y,90,90)

        self.selected = False

def moved_pieces(board_state):
    arr = [0,0,0,0,0,0]
    if board_state[3][7][0] == 0:
        arr[0] = 1
    if board_state[5][7][4] == 0:
        arr[1] = 1
    if board_state[3][7][7] == 0:
        arr[2] = 1
    if board_state[9][0][0] == 0:
        arr[3] = 1
    if board_state[11][0][4] == 0:
        arr[4] = 1
    if board_state[9][0][7] == 0:
        arr[5] = 1
    return arr

def piece_group(board_state):
    pieces = pygame.sprite.Group()
    for i in range(12):
        positions = np.where(np.array(board_state[i]) == 1)
        for j in range(len(positions[0])):
            type = square_occupied(positions[1][j], positions[0][j], board_state)[1]
            pieces.add(Piece(abs(type // 6 - 1), type, 90 * positions[1][j], 90 * positions[0][j]))
    return pieces

def only_legal_moves(board_state):
    return np.where(np.array(legal_moves(board_state)) == 1)[0]

def board_setup():
    pieces = pygame.sprite.Group()
    for i in range(8):
        pieces.add(Piece(1, 0, 90 * i, 540))
    pieces.add(Piece(1, 3, 0, 630))
    pieces.add(Piece(1, 3, 630, 630))
    pieces.add(Piece(1, 1, 90, 630))
    pieces.add(Piece(1, 1, 540, 630))
    pieces.add(Piece(1, 2, 180, 630))
    pieces.add(Piece(1, 2, 450, 630))
    pieces.add(Piece(1, 5, 360, 630))
    pieces.add(Piece(1, 4, 270, 630))
    for i in range(8):
        pieces.add(Piece(0, 6, 90 * i, 90))
    pieces.add(Piece(0, 9, 0, 0))
    pieces.add(Piece(0, 9, 630, 0))
    pieces.add(Piece(0, 7, 90, 0))
    pieces.add(Piece(0, 7, 540, 0))
    pieces.add(Piece(0, 8, 180, 0))
    pieces.add(Piece(0, 8, 450, 0))
    pieces.add(Piece(0, 11, 360, 0))
    pieces.add(Piece(0, 10, 270, 0))
    return pieces

def tiles():
    board = []
    for i in range(8):
        for j in range(8):
            board.append(pygame.Rect(i * 90, j * 90, 90, 90))
    return board

def turn_array(turn_color):
    return [[turn_color for i in range(8)] for j in range(8)]

def get_rook_castle(x,y, pieces):
    for piece in pieces:
        if piece.rect[0] == 90 * x and piece.rect[1] == 90 * y:
            return piece

'''
def castle_moved_piece(piece, castle_moved):
    if piece.type == 3:
        if int(piece.rect[0] / 90) == 0:
            castle_moved[0] = 1
        elif int(piece.rect[0] / 90) == 7:
            castle_moved[2] = 1
    elif piece.type == 5:
        castle_moved[1] = 1
    elif piece.type == 9:
        if int(piece.rect[0] / 90) == 0:
            castle_moved[3] = 1
        elif int(piece.rect[0] / 90) == 7:
            castle_moved[5] = 1
    elif piece.type == 11:
        castle_moved[5] = 1
    return castle_moved
'''


def white_kingside_castle(board_state, castle_moved):
    castle = 0
    through_check = 0
    for i in range(3):
        board = copy.deepcopy(board_state)
        board[5][7][4] = 0
        board[5][7][4 + i] = 1
        if check(board) == 1:
            through_check = 1
    if castle_moved[1] == 0 and castle_moved[2] == 0:
        if through_check == 0:
            if square_occupied(5,7,board_state)[0] == 0 and square_occupied(6,7,board_state)[0] == 0:
                castle = 1
    return turn_array(castle)



def black_kingside_castle(board_state, castle_moved):
    castle = 0
    through_check = 0
    for i in range(3):
        board = copy.deepcopy(board_state)
        board[11][0][4] = 0
        board[11][0][4 + i] = 1
        if check(board) == 1:
            through_check = 1
    if castle_moved[4] == 0 and castle_moved[3] == 0:
        if through_check == 0:
            if square_occupied(5,0,board_state)[0] == 0 and square_occupied(6,0,board_state)[0] == 0:
                castle = 1
    return turn_array(castle)

def black_queenside_castle(board_state, castle_moved):
    castle = 0
    through_check = 0
    for i in range(3):
        board = copy.deepcopy(board_state)
        board[11][0][4] = 0
        board[11][0][4 - i] = 1
        if check(board) == 1:
            through_check = 1
    if castle_moved[4] == 0 and castle_moved[5] == 0:
        if through_check == 0:
            if square_occupied(2,0,board_state)[0] == 0 and square_occupied(3,0,board_state)[0] == 0:
                castle = 1
    return turn_array(castle)

def white_queenside_castle(board_state, castle_moved):
    castle = 0
    through_check = 0
    for i in range(3):
        board = copy.deepcopy(board_state)
        board[5][7][4] = 0
        board[5][7][4 - i] = 1
        if check(board) == 1:
            through_check = 1
    if castle_moved[1] == 0 and castle_moved[0] == 0:
        if through_check == 0:
            if square_occupied(2,7,board_state)[0] == 0 and square_occupied(3,7,board_state)[0] == 0:
                castle = 1
    return turn_array(castle)

# Take winning or equal trades and avoid hanging a piece
# To make a basic bot that makes legal moves with some purpose
def best_move(board_state):
    score = []
    castle_moved = moved_pieces(board_state)
    for black_a in only_legal_moves(board_state):

        scor = 0
        
        board = copy.deepcopy(board_state)
        x, y, x_new, y_new = make_move(black_a, board)

        if square_occupied(x_new,y_new,board)[0]:
            captured_type = square_occupied(x_new,y_new,board)[1]
            black_score = value(captured_type)
        else:
            black_score = 0

        update_board(black_a, board)

        white_score_array = []

        if len(only_legal_moves(board)) == 0:
            white_score_array.append(-math.inf)
        else:
            for white_a in only_legal_moves(board):
                
                x, y, x_new, y_new = make_move(white_a, board)
        
                if square_occupied(x_new,y_new,board)[0]:
                    captured_type = square_occupied(x_new,y_new,board)[1]
                    white_score = value(captured_type)
                else:
                    white_score = 0
    
                white_score_array.append(white_score)

        score.append(black_score - max(white_score_array))
    
    return score

def make_move(a, board_state):
    x = a // 512
    y = (a // 64) % 8
    plane = a % 64
    
    current_type = square_occupied(x,y,board_state)[1]
    
    delta_x = [0,1,1,1,0,-1,-1,-1]
    delta_y = [-1,-1,0,1,1,1,0,-1]
    delta_x_knight = [1,2,2,1,-1,-2,-2,-1]
    delta_y_knight = [-2,-1,1,2,2,1,-1,-2]
    
    if plane < 56:
        dir = plane // 7
        steps = plane % 7 + 1
        x_new = x + steps * delta_x[dir]
        y_new = y + steps * delta_y[dir]
    if plane > 55:
        ind = plane % 8
        x_new = x + delta_x_knight[ind]
        y_new = y + delta_y_knight[ind]

    return x, y, x_new, y_new

def value(piece_type):
    if piece_type in [0,6]:
        value = 1
    elif piece_type in [1,7,2,8]:
        value = 3
    elif piece_type in [3,9]:
        value = 5
    elif piece_type in [4,10]:
        value = 9
    return value

def update_board(a, current_board):
    
    x = a // 512
    y = (a // 64) % 8
    plane = a % 64
    type = square_occupied(x,y,current_board)[1]

    if legal_moves(current_board)[a] == 1:

        x_new = 0
        y_new = 0

        delta_x = [0,1,1,1,0,-1,-1,-1]
        delta_y = [-1,-1,0,1,1,1,0,-1]
        delta_x_knight = [1,2,2,1,-1,-2,-2,-1]
        delta_y_knight = [-2,-1,1,2,2,1,-1,-2]
        if plane < 56:
            dir = plane // 7
            steps = plane % 7 + 1
            x_new = x + steps * delta_x[dir]
            y_new = y + steps * delta_y[dir]
        if plane > 55:
            ind = plane % 8
            x_new = x + delta_x_knight[ind]
            y_new = y + delta_y_knight[ind]
        if square_occupied(x_new,y_new,current_board)[0] == 1:
            current_board[square_occupied(x_new,y_new,current_board)[1]][y_new][x_new] = 0

        current_board[type][y][x] = 0
        current_board[type][y_new][x_new] = 1
        
        if a == 2511:
            current_board[3][7][7] = 0
            current_board[3][7][5] = 1
        elif a == 2539:
            current_board[3][7][0] = 0
            current_board[3][7][3] = 1
        elif a == 2063:
            current_board[9][0][7] = 0
            current_board[9][0][5] = 1
        elif a == 2091:
            current_board[9][0][0] = 0
            current_board[9][0][3] = 1
        elif a in [64,576,1088,1600,2112,2624,3136,3648]:
            auto_queen_x = a // 512
            if square_occupied(x, y, current_board)[1] == 0:
                current_board[0][0][auto_queen_x] = 0
                current_board[4][0][auto_queen_x] = 1
        elif a in [412,924,1436,1948,2460,2972,3484,3996]:
            auto_queen_x = a // 512
            if square_occupied(x, y, current_board)[1] == 6:
                current_board[6][7][auto_queen_x] = 0
                current_board[10][7][auto_queen_x] = 1
        elif a in [71,583,1095,1607,2119,2631,3143]:
            auto_queen_x = a // 512
            if square_occupied(x, y, current_board)[1] == 0:
                current_board[0][0][auto_queen_x + 1] = 0
                current_board[4][0][auto_queen_x + 1] = 1
        elif a in [625,1137,1649,2161,2673,3185,3697]:
            auto_queen_x = a // 512
            if square_occupied(x, y, current_board)[1] == 0:
                current_board[0][0][auto_queen_x - 1] = 0
                current_board[4][0][auto_queen_x - 1] = 1
        elif a in [931,1443,1955,2467,2979,3491,4003]:
            auto_queen_x = a // 512
            if square_occupied(x, y, current_board)[1] == 6:
                current_board[6][7][auto_queen_x - 1] = 0
                current_board[10][7][auto_queen_x - 1] = 1
        elif a in [405,917,1429,1941,2453,2965,3477,3989]:
            auto_queen_x = a // 512
            if square_occupied(x, y, current_board)[1] == 6:
                current_board[6][7][auto_queen_x + 1] = 0
                current_board[10][7][auto_queen_x + 1] = 1
        elif a in [277,789,1301,1813,2325,2837,3349,3861]:
            current_board[0][y][x + 1] = 0
        elif a in [291,803,1315,1827,2339,2851,3363,3875]:
            current_board[0][y][x - 1] = 0
        elif a in [199,711,1223,1735,2247,2759,3271,3783]:
            current_board[6][y][x + 1] = 0
        elif a in [241,753,1265,1777,2289,2801,3313,3825]:
            current_board[6][y][x - 1] = 0
    
        current_board[12] = [[1 - current_board[12][0][0] for i in range(8)] for j in range(8)]

        castle_moved = moved_pieces(current_board)
    
        current_board[13] = white_kingside_castle(current_board, castle_moved)
        current_board[14] = white_queenside_castle(current_board, castle_moved)
        current_board[15] = black_kingside_castle(current_board, castle_moved)
        current_board[16] = black_queenside_castle(current_board, castle_moved)

        if a in [385,897,1409,1921,2433,2945,3457,3969]:
            current_board[18][0][a // 512] = 1
        if a in [93,605,1117,1629,2141,2653,3165,3677]:
            current_board[19][0][a // 512] = 1
        
    return current_board

def init_board():
    
    board_init_state = [
        
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0]],
    
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 1, 0]],
    
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 1, 0, 0]],
    
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 0, 0, 0, 0, 0, 1]],
    
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0]],
    
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0]],
    
        [[0, 0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],
    
        [[0, 1, 0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],
    
        [[0, 0, 1, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],
    
        [[1, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],
    
        [[0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],
    
        [[0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],

        [[1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]],

        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0]],

        [[0, 0, 0, 0, 0, 0, 0, 0]]
   
    ]

    return board_init_state


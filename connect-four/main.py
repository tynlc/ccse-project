# to make matrix of 0's
import numpy as np
import pygame
import sys
import math

# creating the board 
def create_board():
    # background/board 6x7 size
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# importing the bg of the board 
def sqr(x,y,rad):

    img = pygame.image.load('pics/bubbles.png')
    img = pygame.transform.scale(img, rad)
    rect =  img.get_rect()
    rect.centerx = x+50
    rect.top =  y
    screen.blit(img, rect)

# creating the bg of board
def draw_board(board):
    screen.blit(background,(0,100))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            x = c*SQUARESIZE
            y = r *SQUARESIZE + SQUARESIZE
            rad = (SQUARESIZE, SQUARESIZE)
            sqr(x,y,rad)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                x = int(c*SQUARESIZE+SQUARESIZE/2)
                y = height-int(r*SQUARESIZE+SQUARESIZE/2)-35
                sizes = (60,60)
                p1(x,y,sizes)

            elif board[r][c] == 2:
                x = int(c*SQUARESIZE+SQUARESIZE/2)
                y = height-int(r*SQUARESIZE+SQUARESIZE/2)-35
                sizes = (60,60)
                p2(x,y,sizes)

    pygame.display.update()

# flip so that 0 will start at the bottom
def print_board(board):
    print(np.flip(board, 0))

# importing player1 token
def p1(x,y,sizes):
    img = pygame.image.load('pics/spongebob.png')
    img = pygame.transform.scale(img, sizes)
    rect =  img.get_rect()
    rect.centerx =  x
    rect.top =  y
    screen.blit(img, rect)

# importing player2 token
def p2(x,y,sizes):

    img = pygame.image.load('pics/patrick.png')
    img = pygame.transform.scale(img, sizes)
    rect =  img.get_rect()
    rect.centerx =  x
    rect.top =  y
    screen.blit(img, rect)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

# so that players will not pass the 5th row
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# para musampaw ang token
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check all horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check all vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# font for text 
def myfont(fontsize):
    return pygame.font.SysFont("bubble_soap", fontsize)

# start of the game
def main_menu():
    run = True
    while run:
        screen.blit(image,(0,0))
        sizes = (60,60)
        p1(80,165,sizes)
        p2(640,170,sizes)
        welfont = pygame.font.SysFont("sketch_3d", 170)
        welmsg =  welfont.render('Dot', 10, YELLOW, screen)
        screen.blit(welmsg, (20, 200))
        welmsg2 = welfont.render('Net', 10, PINK, screen)
        screen.blit(welmsg2, (350, 200))
        welfont3 = pygame.font.SysFont("rockness", 50)
        welmsg3 =  welfont3.render('(Press any key to continue)', 10, (0, 0, 0), screen)
        screen.blit(welmsg3, (130, 370))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                screen.blit(bg_up,(0,0))
                draw_board(board)
                main()
                run = False

    pygame.quit()

# the flow of the game
def main():

    print_board(board)
    game_over = False
    turn = 0
    
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                screen.blit(bg_up,(0,0))
                posx = event.pos[0]
                if turn == 0:
                    label = myfont(30).render("SPONGEBOB'S TURN !", 1, YELLOW)
                    screen.blit(label, (20, 0))
                    sizes = (60,60)
                    p1(posx,20,sizes)

                else:
                    label = myfont(30).render("PATRICK'S TURN !", 2, PINK)
                    screen.blit(label, (430, 0))
                    sizes = (60,60)
                    p2(posx,20,sizes)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            screen.blit(bg_up,(0,0))
                            winner = "SPONGEBOB WINS !"
                            winner_pic = 1
                            game_over = True

                # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            screen.blit(bg_up,(0,0))
                            winner = "PATRICK WINS !"
                            winner_pic = 2
                            game_over = True

                print_board(board)
                draw_board(board)
            
                turn += 1
                turn = turn % 2


                if game_over:
                    pygame.time.wait(1000)
                    screen.blit(image,(0,0))
                    over = pygame.font.SysFont("rockness", 130)
                    over_msg =  over.render('GAME OVER', 10, BLACK, screen)
                    screen.blit(over_msg, (30, 160))
                    win_msg =  myfont(60).render(winner, 10, BLACK, screen)
                    screen.blit(win_msg, (110, 330))
                    if winner_pic == 1:
                        sizes = (250,250)
                        p1(360,400, sizes)
                        pygame.mixer.music.load('music/spongebob_win.mp3')
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(-1)
                    else:
                        sizes = (250,250)
                        p2(360,400, sizes)
                        pygame.mixer.music.load('music/patrick_win.mp3')
                        pygame.mixer.music.set_volume(1)
                        pygame.mixer.music.play(-1)
                    pygame.display.update()
                    pygame.time.wait(10000) 

# colors
YELLOW = (232, 177, 0)
PINK = (248, 131, 121)
BLACK = (0, 0, 0)

# setting row and column
ROW_COUNT = 6
COLUMN_COUNT = 7

# importing backgrounds
bg_up = pygame.image.load('pics/bg_up.jpg')
bg_up = pygame.transform.scale(bg_up,(700,100))
image = pygame.image.load('pics/menu.jpg')
image = pygame.transform.scale(image, (700, 700))
background = pygame.image.load('pics/bg_down.jpg')
background = pygame.transform.scale(background,(700,600))

board = create_board()

# importing musics
pygame.mixer.init(44100,16,2,4096)
pygame.init()
pygame.mixer.music.load('music/aloha.mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# title of the game
pygame.display.set_caption('DotNet')

# sizes of squares
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
pygame.display.update()      

# Calling the function to start the game
main_menu()

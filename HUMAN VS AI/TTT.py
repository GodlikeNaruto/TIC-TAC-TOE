import pygame as pg, sys
from pygame.locals import *
import time, random

width = 400
height = 400
white = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
line_color = (10, 10, 10)

# initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

# loading the images
opening = pg.image.load('tic tac opening.png')
x_img = pg.image.load('x.png')
o_img = pg.image.load('o.png')

# resizing images
x_img = pg.transform.scale(x_img, (80, 80))
o_img = pg.transform.scale(o_img, (80, 80))
opening = pg.transform.scale(opening, (width, height + 100))

XO = None  # -1 is X-player, 1 is O-player
move = None # numbers from 0 to 8

winner = None
draw = False

    # TicTacToe 3x3 board
TTT= [0,0,0,0,0,0,0,0,0]
    # game field is shared on 9 cells with determination of each one from left to right in upper,middle & lower row:
    # 0,1,2 - upper row
    # 3,4,5 - middle row
    # 6,7,8 - lower row
    # totaly = 3x3 field = 9 numbers (from 0 to 8 considering that list [TTT] starts with 0 position)
def game_opening():
    screen.fill(white)
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1.5)
    screen.fill(white)

    # Drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    # Drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)

    game_status()
def game_status(): # status of the game

    if winner is None and XO == -1:
        message = "X's Turn"
    if winner == -1:
        message = "X won!"

    if winner is None and XO == 1:
        message = "0's Turn"
    if winner == 1:
        message = "0 won!"
    if draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()
    time.sleep(0.4)
def check_win(): # check winner and drawing the appropriate lines
    global TTT, winner, draw

    # check for winning rows
    for row in range(0, 7, 3):  # jump through 3 in TTT list
        if ((TTT[row] == TTT[row + 1] == TTT[row + 2]) and (TTT[row] != 0)):
            # this row won
            winner = TTT[row]
            pg.draw.line(screen, (250, 0, 0), (0, (row/3 + 1) * height / 3 - height / 6), \
                         (width, (row/3 + 1) * height / 3 - height / 6), 6)
            break

    # check for winning columns
    for col in range(0, 3, 1):  # jump through 1 in TTT list
        if (TTT[col] == TTT[col + 3] == TTT[col + 6]) and (TTT[col] != 0):
            # this column won
            winner = TTT[col]
            # draw winning line
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0), \
                         ((col + 1) * width / 3 - width / 6, height), 6)
            break

    # check for diagonal winners
    if (TTT[0] == TTT[4] == TTT[8]) and (TTT[0] != 0):
        # game won diagonally left to right
        winner = TTT[0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 6)

    if (TTT[2] == TTT[4] == TTT[6]) and (TTT[2] != 0):
        # game won diagonally right to left
        winner = TTT[2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 6)

    if TTT.count(0) == 0 and winner is None:  # all cells are filled in
        draw = True

    game_status()
    #time.sleep(0.5)
def DrawXO(): # drawing of X or O, and after a sign will be reversed (XO => - XO) for player changing
    global TTT, XO, move
    TTT[move] = XO
    if move == 0:
        posx = 30
        posy = 30
    if move == 1:
        posx = width / 3 + 30
        posy = 30
    if move == 2:
        posx = width / 3 * 2 + 30
        posy = 30

    if move == 3:
        posx = 30
        posy = height / 3 + 30
    if move == 4:
        posx = width / 3 + 30
        posy = height / 3 + 30
    if move == 5:
        posx = width / 3 * 2 + 30
        posy = height / 3 + 30

    if move == 6:
        posx = 30
        posy = height / 3 * 2 + 30
    if move == 7:
        posx = width / 3 + 30
        posy = height / 3 * 2 + 30
    if move == 8:
        posx = width / 3 * 2 + 30
        posy = height / 3 * 2 + 30

    if XO == -1:
        screen.blit(x_img, (posx, posy))
    else:
        screen.blit(o_img, (posx, posy))
    XO = -1*XO
    pg.display.update()
    check_win()
def check_moves(): # finding the best cell for the next computer's move
    global TTT, move
    mov_map = [0, 0, 0, 0, 0, 0, 0, 0, 0] # map of the moves before each computer's move in current situation
    move = None
    # check for winning rows
    # the sum of the moduli of the current value and the winning cell of the checked player, and then multiply them by the sign of the checked player
    # in the most cases: zero + 1 or -1 (current player), but if the cell has two or three winners simultaneously, the module of the value must be 2 or 3 (-2 or -3)
    for row in range(0, 7, 3):  # jump through 1 in TTT list
        r=TTT[row] + TTT[row + 1] + TTT[row + 2]
        if abs(r) == 2:
            if TTT[row] == 0:
                mov = row
                mov_map[mov] = (abs(mov_map[mov])+abs(int((r) / 2)))*int((r) / 2) #the sum of winning's module both of players & multiple on the current player's sign
            elif TTT[row + 1] == 0:
                mov = row + 1
                mov_map[mov] = (abs(mov_map[mov])+abs(int((r) / 2)))*int((r) / 2)
            elif TTT[row + 2] == 0:
                mov = row + 2
                mov_map[mov] = (abs(mov_map[mov])+abs(int((r) / 2)))*int((r) / 2)

    # check for winning columns
    for col in range(0, 3, 1):  # jump through 1 in TTT list
        c=TTT[col] + TTT[col + 3] + TTT[col + 6]
        if abs(c) == 2:
            if TTT[col] == 0:
                mov = col
                mov_map[mov] = (abs(mov_map[mov])+abs(int((c) / 2)))*int((c) / 2)
            elif TTT[col + 3] == 0:
                mov = col + 3
                mov_map[mov] = (abs(mov_map[mov])+abs(int((c) / 2)))*int((c) / 2)
            elif TTT[col + 6] == 0:
                mov = col + 6
                mov_map[mov] = (abs(mov_map[mov]) + abs(int((c) / 2))) * int((c) / 2)

    # check for diagonal winners: L>R
    d_Lr=TTT[0] + TTT[4] + TTT[8]
    if abs(d_Lr) == 2:
        if TTT[0] == 0:
            mov = 0
            mov_map[mov] = (abs(mov_map[mov])+abs(int((d_Lr) / 2)))*int((d_Lr) / 2)
        elif TTT[4] == 0:
            mov = 4
            mov_map[mov] = (abs(mov_map[mov])+abs(int((d_Lr) / 2)))*int((d_Lr) / 2)
        elif TTT[8] == 0:
            mov = 8
            mov_map[mov] = (abs(mov_map[mov])+abs(int((d_Lr) / 2)))*int((d_Lr) / 2)

        # check for diagonal winners: R>L
    d_Rl=TTT[2] + TTT[4] + TTT[6]
    if abs(d_Rl) == 2:
        if TTT[2] == 0:
            mov = 2
            mov_map[mov] = (abs(mov_map[mov])+abs(int((d_Rl) / 2)))*int((d_Rl) / 2)
        elif TTT[4] == 0:
            mov = 4
            mov_map[mov] = (abs(mov_map[mov])+abs(int((d_Rl) / 2)))*int((d_Rl) / 2)
        elif TTT[6] == 0:
            mov = 6
            mov_map[mov] = (abs(mov_map[mov])+abs(int((d_Rl) / 2)))*int((d_Rl) / 2)

# if one winner in one cell
    if mov_map.count(XO) > 0 and mov_map.count(-1*XO) == 0: #current player must choose his own square if the opponent hasn't a winning cell
        move = mov_map.index(XO)
    if mov_map.count(-1*XO) > 0 and mov_map.count(XO) == 0: #current player must choose opponent's square if the there isn't his own winning cell
        move = mov_map.index(-1*XO)
    if mov_map.count(XO) > 0 and mov_map.count(-1*XO) > 0: # current player must choose his own square if the opponent has a winning cell as well
        move = mov_map.index(XO)

# if two winners or double one are in one cell - the always preference goes to current player
    if mov_map.count(2) > 0:
        move = mov_map.index(2)
    if mov_map.count(-2) > 0:
        move = mov_map.index(-2)

def user_click(): # mouse click
    global move
    move = None
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()
    # get x,y of mouse click (cell 1-9)
    if (y < height / 3) and (x < width / 3):
        move = 0
    elif (y < height / 3) and (x < width / 3 * 2):
        move = 1
    elif (y < height / 3) and (x < width):
        move = 2

    elif (y < height / 3 * 2) and (x < width / 3):
        move = 3
    elif (y < height / 3 * 2) and (x < width / 3 * 2):
        move = 4
    elif (y < height / 3 * 2) and (x < width):
        move = 5

    elif (y < height) and (x < width / 3):
        move = 6
    elif (y < height) and (x < width / 3 * 2):
        move = 7
    elif (y < height) and (x < width):
        move = 8
def reset_game(): # reset and start a new game
    global TTT, winner, XO, draw
    time.sleep(1)
    XO = -1
    draw = False
    winner = None
    TTT= [0,0,0,0,0,0,0,0,0]
    game_opening()
    game_status()
def X_player(): # Х - player
    global TTT, XO, move, winner, draw

    while (True):  # run the game loop forever
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if XO == -1: # X's move
                if event.type == MOUSEBUTTONDOWN:
                    user_click()  # click mouse button for Х's move
                    if move == None:
                        continue
                    else:
                        if (TTT[move] == 0):
                            DrawXO()
            if XO == 1 and draw is False and winner is None: # O's move
                check_moves()  # check for XX, X_X, OO, O_O
                if move is None:
                    while True:
                        if TTT[4] == 0:  # protection from the fool (when a rival makes typical triangle of "X")
                            move = 4
                            break
                        else:  # a move for good luck, gives a chance to play fair without algorithm
                            move = random.randint(0, 8)
                            if TTT[move] == 0:
                                break
                DrawXO()

        if (winner or draw):
            reset_game()
        pg.display.update()
        CLOCK.tick(fps)
def O_player(): # O - player
    global TTT, XO, move, winner, draw

    while (True):  # run the game loop forever
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if XO == -1:
                check_moves()  # check for XX, X_X, OO, O_O
                if move is None:
                    while True:
                        move = random.randint(0, 8)
                        if TTT[move] == 0:
                            break
                DrawXO()
            if XO == 1 and draw is False and winner is None:
                if event.type == MOUSEBUTTONDOWN:
                    user_click()  # press mouse button for one move X and O-response
                    if move == None:
                        continue
                    else:
                        if (TTT[move] == 0):
                            DrawXO()
        if (winner or draw):
            reset_game()
        pg.display.update()
        CLOCK.tick(fps)
def menu_XO(): # menu = picture for X or O choice
    screen.fill(white)
    # Drawing vertical lines
    pg.draw.line(screen, RED, (width / 3, height/3), (width / 3, height/3*2), 4)
    pg.draw.line(screen, RED, (width / 3 * 2, height/3), (width / 3 * 2, height/3*2), 4)
    pg.draw.line(screen, RED, (1, height / 3), (1, height / 3 * 2), 4)
    pg.draw.line(screen, RED, (width-3, height / 3), (width-3, height / 3 * 2), 4)
    # Drawing horizontal lines
    pg.draw.line(screen, RED, (0, height / 3), (width/3+2, height / 3), 4)
    pg.draw.line(screen, RED, (0, height / 3 * 2), (width/3+2, height / 3 * 2), 4)
    pg.draw.line(screen, RED, (width / 3*2, height / 3), (width, height / 3), 4)
    pg.draw.line(screen, RED, (width / 3*2, height / 3 * 2), (width, height / 3 * 2), 4)
    screen.blit(x_img, (30, 160))
    screen.blit(o_img, (290, 160))
    font = pg.font.Font(None, 80)
    text = font.render("X or O ?", 1, (255, 255, 255))
    # copy the rendered message onto the board
    screen.fill((RED), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()
def menu_click(): # user click X or O player option
    global XO
    XO = None
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()
    # get x,y of mouse click (cell X or O)

    if (y < height / 3 * 2) and (y > height / 3 * 1) and (x < width / 3) and (x > 0):
        XO = -1
    elif (y < height / 3 * 2) and (y > height / 3 * 1) and (x < width) and (x > width / 3 * 2):
        XO = 1 

while XO is None:  # run the menu loop forever
    for event in pg.event.get():
        menu_XO()
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            menu_click()  # press mouse button to choice X and O player option
            if XO == None:
                continue
            else:
                if XO != None:
                    if XO == -1:
                        message = "X - player"
                    if XO == 1:
                        message = "O - player"

                    font = pg.font.Font(None, 60)
                    text = font.render(message, 1, (255, 255, 255))

                    # copy the rendered message onto the board
                    screen.fill((BLACK), (0, 400, 500, 100))
                    text_rect = text.get_rect(center=(width / 2, 500 - 50))
                    screen.blit(text, text_rect)
                    pg.display.update()
                    time.sleep(1.5)
                    break

game_opening()

if XO==-1:
    X_player() # X - player
elif XO==1:
    XO=-1 # changing sign again to start comp. X first
    O_player() # O - player
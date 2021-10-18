"""
This is our main driver file. It will be responsible for handling user input and displaying current GameState object.
"""

import pygame as p
import sys
from pygame.event import set_blocked
from pygame.locals import *
import ChessEngine
import random
import time


WIDTH = HEIGHT = 512
DIMESION = 8 #dimensions of the chess board are 8x8
SQ_SIZE = HEIGHT // DIMESION
MAX_FPS = 15 #for animations later on
IMAGES = {}

availableMoves = []#avaible moves for selected piece

rCheckMoves = []
cCheckMoves = []
#keep track of if a pawn has moved from its starting position for 2 forward move
wP0 = True
wP1 = True
wP2 = True
wP3 = True
wP4 = True
wP5 = True
wP6 = True
wP7 = True

bP0 = True
bP1 = True
bP2 = True
bP3 = True
bP4 = True
bP5 = True
bP6 = True
bP7 = True


'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("ChessImages/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note: We can access an image by saying 'IMAGES['wP']'

'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    global gs
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages() #only do this once, before the while loop
    running = True
    game_over = False
    sqSelected = () # not square is selected
    playerClicks = [] #keep track of player clicks
    drawGameState(screen, gs)
    while running:
        for e in p.event.get():
            #White's turn
            if e.type == p.MOUSEBUTTONDOWN and game_over == False:
                if e.button == 1:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    piece = gs.board[row][col]
                    if sqSelected == (row, col): #the user clicked the same square twice
                        sqSelected = ()
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)#append for both 1st and 2nd clicks
                    if len(playerClicks) == 2: #after 2 clicks
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                        sqSelected = () #reset clicks
                        drawGameState(screen, gs)
                        playerClicks = []

            if e.type == p.QUIT:
                running = False
            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        
        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                print("Black wins by checkmate")
            else:
                print("White wins by checkmate")

        elif gs.stalemate:
            game_over = True
            print("Stalemate")
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all the graphics within a current game state.
'''
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw pieces on top of those sqaures

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMESION):
        for c in range(DIMESION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMESION):
        for c in range(DIMESION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

            
if __name__ == '__main__':
    main()
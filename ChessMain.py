"""
This is our main driver file. It will be responsible for handling user input and displaying current GameState object.
"""

import pygame as p
import sys
from pygame.event import set_blocked
from pygame.locals import *
import ChessEngine


WIDTH = HEIGHT = 512
DIMESION = 8 #dimensions of the chess board are 8x8
SQ_SIZE = HEIGHT // DIMESION
MAX_FPS = 15 #for animations later on
IMAGES = {}

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
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    selected = [-1, -1]  #assign selected a coordinate value so I don't get any variable unassigned errors
    loadImages() #only do this once, before the while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    print(mx)
                    print(my)
                    selected = selectPiece(mx, my, gs.board, screen)

            if e.type == p.QUIT:
                running = False

        drawGameState(screen, gs, selected)
        
        mx, my = p.mouse.get_pos() #gets mouse position, only captures position when cursor is in pygame window

        clock.tick(MAX_FPS)
        p.display.flip()

'''
On click, go through all the pieces on the board and see which is touching the cursor so it can be selected. returns selected piece coordinates
'''
def selectPiece(mx, my, board, screen):
    for r in range(DIMESION):
        for c in range(DIMESION):
            piece = board[r][c] #Get name of piece
            #print(piece)
            if piece != "--" and p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE).collidepoint(mx, my): #see if the cursor coords are within the piece's square
                p.draw.rect(screen, p.Color("orange"), p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                selected = [r, c]
                #print(selected)
                return selected
            elif piece == "--":
                selected = [-1, 1]
                #print(selected)
    return selected
            
'''
Responsible for all tje graphics within a current game state.
'''
def drawGameState(screen, gs, selected):
    drawBoard(screen, selected) #draw squares on the board
    #add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) #draw pieces on top of those sqaures

'''
Draw the squares on the board. The top left square is always light.
'''
def drawBoard(screen, selected):
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMESION):
        for c in range(DIMESION):
            if r == selected[0] and c == selected[1]:
                p.draw.rect(screen, p.Color("orange"), p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
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
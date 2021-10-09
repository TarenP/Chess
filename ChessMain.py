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

#keep track of if a pawn has moved from its starting position for 2 forward move
wP0 = False
wP1 = False
wP2 = False
wP3 = False
wP4 = False
wP5 = False
wP6 = False
wP7 = False


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
    selectedCoord = [-1, -1]  #assign selected a coordinate value so I don't get any variable unassigned errors
    selectedPiece = "--" #assign selected to nothing by default
    loadImages() #only do this once, before the while loop
    running = True
    drawGameState(screen, gs)
    while running:
        for e in p.event.get():
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    #print(mx)
                    #print(my)
                    selectedCoord, selectedPiece = selectPiece(mx, my, gs.board, screen)
                    possibleMoves(selectedCoord, gs, screen, selectedPiece)

            if e.type == p.QUIT:
                running = False
        mx, my = p.mouse.get_pos() #gets mouse position, only captures position when cursor is in pygame window

        clock.tick(MAX_FPS)
        p.display.flip()

'''
On click, go through all the pieces on the board and see which is touching the cursor so it can be selected. returns selected piece coordinates
'''
def selectPiece(mx, my, board, screen):
    drawBoard(screen) #remove the orange square from the board because a new one is going to be chosen
    drawPieces(screen, board) #place pieces on top of newly drawn board
    for r in range(DIMESION):
        for c in range(DIMESION):
            piece = board[r][c] #Get name of piece
            #print(piece)
            #Only want the user to move white pieces
            if piece[0] != "b" and piece != "--" and p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE).collidepoint(mx, my): #see if the cursor coords are within the piece's square
                p.draw.rect(screen, p.Color("orange"), p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                drawPieces(screen, board)
                selectedCoord = [r, c]
                #print(selected)
                return selectedCoord, piece
            elif piece == "--":
                selectedCoord = [-1, 1]
                #print(selected)
                
    return selectedCoord, piece

'''
Logic for possible moves for each piece depending on piece type
'''
def possibleMoves(selectedCoord, gs, screen, selectedPiece):
    board = gs.board
    #drawPieces(screen, gs.board)
    #selectedCoord[0] = row; selectedCoord[1] = column
    if selectedPiece[1] == "P":
        pawnName = 'wP' + str(selectedCoord[1])
        print(pawnName)
        if pawnName == False:
            selectedCoord[0] -= 2
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, board)
            selectedCoord[0] += 1
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, board)
        else:
            selectedCoord[0] -= 1
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, board)
            
            
'''
Draw the possible moves. Used by possibleMoves to create a visual of the possible moves.
Choice for color so I can easily change it so the ending spot for each possible move is a different color than the path
'''
def drawPossibleMoves(coordinate, color, screen, board):
    p.draw.rect(screen, p.Color(color), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
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
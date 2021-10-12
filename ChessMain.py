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
    selectedCoord = [-1, -1]  #assign selected a coordinate value so I don't get any variable unassigned errors
    selectedPiece = "--" #assign selected to nothing by default
    loadImages() #only do this once, before the while loop
    running = True
    alrSelected = False #Once a piece is selected, it has to be moved.
    drawGameState(screen, gs)
    while running:
        mx, my = p.mouse.get_pos() #gets mouse position, only captures position when cursor is in pygame window
        for e in p.event.get():
            #White's turn
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1 and alrSelected == False and gs.whiteToMove == True:
                    alrSelected = True
                    #print(mx)
                    #print(my)
                    selectedCoord, selectedPiece = selectPiece(mx, my, gs.board, screen)
                    if selectedCoord == [-1, -1]:
                        alrSelected = False
                    possibleMoves(selectedCoord, gs, screen, selectedPiece)
                    if availableMoves == []:
                        alrSelected = False
                else:
                    endCoord = movePiece(availableMoves, mx, my)
                    if endCoord == None:
                        break
                    #print(selectedCoord)
                    #print(endCoord)
                    move = ChessEngine.Move(selectedCoord, endCoord, gs.board)
                    #print(gs.moveLog)
                    gs.makeMove(move)
                    #print(gs.board)
                    drawGameState(screen, gs)
                    checkScanner(screen)
                    alrSelected = False

            if e.type == p.QUIT:
                running = False

        #Black's Turn
        if gs.whiteToMove == False and alrSelected == False:
            blackPieces = []
            alrSelected = True
            #Get positions of all black pieces on board
            for r in range(DIMESION):
                for c in range(DIMESION):
                    piece = gs.board[r][c]
                    if piece[0] == "b":
                        blackPieces.append(r)
                        blackPieces.append(c)
            rand_idx = random.randrange(len(blackPieces))
            if rand_idx % 2 != 0:
                c = blackPieces[rand_idx]
                r = blackPieces[rand_idx - 1]
            else:
                c = blackPieces[rand_idx + 1]
                r = blackPieces[rand_idx]
            selectedPiece = gs.board[r][c]
            selectedCoord = [r, c]
            #print("selected Coord " + str(selectedCoord))
            drawPieces(screen, gs.board)
            possibleMoves(selectedCoord, gs, screen, selectedPiece)
            if availableMoves == []:
                alrSelected = False
            else:
                p.draw.rect(screen, p.Color("orange"), p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                endCoord = movePiece(availableMoves, mx, my)
                p.draw.rect(screen, p.Color("blue"), p.Rect(endCoord[1]*SQ_SIZE, endCoord[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                if endCoord == None:
                    alrSelected = False
                move = ChessEngine.Move(selectedCoord, endCoord, gs.board)
                gs.makeMove(move)
                drawGameState(screen, gs)
                checkScanner(screen)
                alrSelected = False
        clock.tick(MAX_FPS)
        p.display.flip()

'''
On click, go through all the pieces on the board and see which is touching the cursor so it can be selected. returns selected piece coordinates
'''
def selectPiece(mx, my, board, screen):
    drawGameState(screen, gs) #remove the orange square from the board because a new one is going to be chosen #place pieces on top of newly drawn board
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
                selectedCoord = [-1, -1]
                #print(selected) 
    return selectedCoord, piece

'''
Logic for possible moves for each piece depending on piece type
'''
def possibleMoves(selectedCoord, gs, screen, selectedPiece):
    board = gs.board

    global wP0, wP1,wP2,wP3,wP4,wP5,wP6,wP7, bP0, bP1,bP2,bP3,bP4,bP5,bP6,bP7, availableMoves

    availableMoves = []
    #drawPieces(screen, gs.board)
    #selectedCoord[0] = row; selectedCoord[1] = column
    #check if the pawn has already been moved
    #change coordinates to display the possible moves then revert the coordinates for future use
    #print(selectedPiece)
    if selectedPiece[1] == "P":
        if gs.whiteToMove == True:
            if ('wP' + str(selectedCoord[1])) == "wP0":
                if wP0 == True:
                    selectedCoord[0] -= 2
                    drawPossibleMovesP(selectedCoord, " ", screen, gs.board, wP0)
                    selectedCoord[0] += 2
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP0 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('wP' + str(selectedCoord[1])) == "wP1":
                if wP1 == True:
                    selectedCoord[0] -= 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, wP1)
                    selectedCoord[0] += 2
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP1 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board,False)
                    selectedCoord[0] += 1
            elif ('wP' + str(selectedCoord[1])) == "wP2":
                if wP2 == True:
                    selectedCoord[0] -= 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, wP2)
                    selectedCoord[0] += 2
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP2 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
            elif ('wP' + str(selectedCoord[1])) == "wP3":
                if wP3 == True:
                    selectedCoord[0] -= 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, wP3)
                    selectedCoord[0] += 2
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP3 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
            elif ('wP' + str(selectedCoord[1])) == "wP4":
                if wP4 == True:
                    selectedCoord[0] -= 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, wP4)
                    selectedCoord[0] += 2
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP4 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
            elif ('wP' + str(selectedCoord[1])) == "wP5":
                if wP5 == True:
                    selectedCoord[0] -= 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, wP5)
                    selectedCoord[0] += 2
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP5 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
            elif ('wP' + str(selectedCoord[1])) == "wP6":
                if wP6 == True:
                    selectedCoord[0] -= 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, wP6)
                    selectedCoord[0] += 2
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP6 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
            elif ('wP' + str(selectedCoord[1])) == "wP7":
                if wP7 == True:
                    print(selectedCoord)
                    selectedCoord[0] -= 2
                    print(selectedCoord)
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, wP7)
                    print(selectedCoord)
                    selectedCoord[0] += 2
                    print(selectedCoord)
                    selectedCoord[0] -= 1
                    print(selectedCoord)
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
                    wP7 = False
                else:
                    selectedCoord[0] -= 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] += 1
        else:
            #Black Pawns
            if ('bP' + str(selectedCoord[1])) == "bP0":
                if bP0 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP0)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP0 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('bP' + str(selectedCoord[1])) == "bP1":
                if bP1 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP1)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP1 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('bP' + str(selectedCoord[1])) == "bP2":
                if bP2 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP2)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP2 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('bP' + str(selectedCoord[1])) == "bP3":
                if bP3 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP3)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP3 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('bP' + str(selectedCoord[1])) == "bP4":
                if bP4 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP4)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP4 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('bP' + str(selectedCoord[1])) == "bP5":
                if bP5 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP5)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP5 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('bP' + str(selectedCoord[1])) == "bP6":
                if bP6 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP6)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP6 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
            elif ('bP' + str(selectedCoord[1])) == "bP7":
                if bP7 == True:
                    selectedCoord[0] += 2
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, bP7)
                    selectedCoord[0] -= 2
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
                    bP7 = False
                else:
                    selectedCoord[0] += 1
                    drawPossibleMovesP(selectedCoord, "cadetblue2", screen, gs.board, False)
                    selectedCoord[0] -= 1
    
    elif selectedPiece[1] == "R":
        revert = 0
        keepGoing = True
        while selectedCoord[0] > 0 and keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
            revert += 1       
            selectedCoord[0] -= 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += revert

        keepGoing = True
        revert = 0
        while selectedCoord[0] < 7 and keepGoing == True:
            revert += 1       
            selectedCoord[0] += 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= revert

        revert = 0
        keepGoing = True
        while selectedCoord[1] > 0 and keepGoing == True:
            revert += 1       
            selectedCoord[1] -= 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[1] += revert

        keepGoing = True
        revert = 0
        while selectedCoord[1] < 7 and keepGoing == True:
            revert += 1       
            selectedCoord[1] += 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[1] -= revert

    elif  selectedPiece[1] == "B":
        revert = 0
        keepGoing = True
        if gs.whiteToMove == True:
            #diagnol up-right
            try:
                while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                    revert += 1       
                    selectedCoord[0] -= 1
                    selectedCoord[1] += 1
                    keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
            except:
                pass
            keepGoing = False
            selectedCoord[0] += revert
            selectedCoord[1] -= revert

            revert = 0
            keepGoing = True
            #diagnol up-left
            try:
                while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                    revert += 1       
                    selectedCoord[0] -= 1
                    selectedCoord[1] -= 1
                    keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
            except:
                pass
            keepGoing = False
            selectedCoord[0] += revert
            selectedCoord[1] += revert

            revert = 0
            keepGoing = True
            #diagnol down-right
            try:
                while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                    revert += 1       
                    selectedCoord[0] += 1
                    selectedCoord[1] += 1
                    keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
            except:
                pass
            keepGoing = False
            selectedCoord[0] -= revert
            selectedCoord[1] -= revert

            revert = 0
            keepGoing = True
            #diagnol down-left
            try:
                while keepGoing == True:
                    revert += 1       
                    selectedCoord[0] += 1
                    selectedCoord[1] -= 1
                    keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
            except:
                pass
            keepGoing = False
            selectedCoord[0] -= revert
            selectedCoord[1] += revert

    elif selectedPiece[1] == "N":
        #diagnol up-right
        selectedCoord[0] -= 2
        selectedCoord[1] += 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += 2
        selectedCoord[1] -= 1

        #diagnol up-left
        selectedCoord[0] -= 2
        selectedCoord[1] -= 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += 2
        selectedCoord[1] += 1

        #diagnol down-right 
        selectedCoord[0] += 2
        selectedCoord[1] += 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 2
        selectedCoord[1] -= 1

        #diagnol down-left
        selectedCoord[0] += 2
        selectedCoord[1] -= 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 2
        selectedCoord[1] += 1

        #diagnol left-up
        selectedCoord[0] += 1
        selectedCoord[1] -= 2
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 1
        selectedCoord[1] += 2

        #diagnol left-down
        selectedCoord[0] -= 1
        selectedCoord[1] -= 2
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += 1
        selectedCoord[1] += 2

        #diagnol right-up
        selectedCoord[0] -= 1
        selectedCoord[1] += 2
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += 1
        selectedCoord[1] -= 2

        #diagnol right-down
        selectedCoord[0] += 1
        selectedCoord[1] += 2
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 1
        selectedCoord[1] -= 2

        #diagnol up-left
        selectedCoord[0] += 1
        selectedCoord[1] -= 2
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 1
        selectedCoord[1] += 2

    elif selectedPiece[1] == "Q":
        #Rook attributes
        revert = 0
        keepGoing = True
        while selectedCoord[0] > 0 and keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
            revert += 1       
            selectedCoord[0] -= 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += revert

        keepGoing = True
        revert = 0
        while selectedCoord[0] < 7 and keepGoing == True:
            revert += 1       
            selectedCoord[0] += 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= revert

        revert = 0
        keepGoing = True
        while selectedCoord[1] > 0 and keepGoing == True:
            revert += 1       
            selectedCoord[1] -= 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[1] += revert

        keepGoing = True
        revert = 0
        while selectedCoord[1] < 7 and keepGoing == True:
            revert += 1       
            selectedCoord[1] += 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[1] -= revert

        #Bishop attributes
        revert = 0
        keepGoing = True
        #diagnol up-right
        try:
            while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                revert += 1       
                selectedCoord[0] -= 1
                selectedCoord[1] += 1
                keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        except:
            pass
        keepGoing = False
        selectedCoord[0] += revert
        selectedCoord[1] -= revert

        revert = 0
        keepGoing = True
        #diagnol up-left
        try:
            while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                revert += 1       
                selectedCoord[0] -= 1
                selectedCoord[1] -= 1
                keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        except:
            pass
        keepGoing = False
        selectedCoord[0] += revert
        selectedCoord[1] += revert

        revert = 0
        keepGoing = True
        #diagnol down-right
        try:
            while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                revert += 1       
                selectedCoord[0] += 1
                selectedCoord[1] += 1
                keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        except:
            pass
        keepGoing = False
        selectedCoord[0] -= revert
        selectedCoord[1] -= revert

        revert = 0
        keepGoing = True
        #diagnol down-left
        try:
            while keepGoing == True:
                revert += 1       
                selectedCoord[0] += 1
                selectedCoord[1] -= 1
                keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        except:
            pass
        keepGoing = False
        selectedCoord[0] -= revert
        selectedCoord[1] += revert

    elif  selectedPiece[1] == "K":
        #Straight moves
        selectedCoord[0] -= 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += 1
        selectedCoord[0] += 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 1
        selectedCoord[1] -= 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[1] += 1
        selectedCoord[1] += 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[1] -= 1

        #Diagnol Moves
        selectedCoord[0] -= 1
        selectedCoord[1] -= 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += 1
        selectedCoord[1] += 1
        selectedCoord[0] += 1
        selectedCoord[1] += 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 1
        selectedCoord[1] -= 1
        selectedCoord[0] += 1
        selectedCoord[1] -= 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] -= 1
        selectedCoord[1] += 1
        selectedCoord[0] -= 1
        selectedCoord[1] += 1
        if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
            drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[0] += 1
        selectedCoord[1] -= 1


'''
Draw the possible moves. Used by possibleMoves to create a visual of the possible moves.
Choice for color so I can easily change it so the ending spot for each possible move is a different color than the path
Checks if another piece is blocking the path
'''
def drawPossibleMoves(coordinate, color, screen, board):
    global availableMoves
    if coordinate[0] < 0 or coordinate[0] > 7:
        return False
    if coordinate[1] < 0 or coordinate[1] > 7:
        return False
    piece = board[coordinate[0]][coordinate[1]]
    #print("piece " + str(piece))
    #print("piece's coord " + str(coordinate))
    if gs.whiteToMove == True:
        if piece[0] != "w": #It isn't a valid move to attack your own color
            availableMoves.append(coordinate[0])
            availableMoves.append(coordinate[1])
        if piece == "--":
            p.draw.rect(screen, p.Color(color), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            return True
        if piece[0] == "b":
            p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            drawPieces(screen, board)
            return False
        else:
            return False
    else:
        if piece[0] != "b": #It isn't a valid move to attack your own color
            availableMoves.append(coordinate[0])
            availableMoves.append(coordinate[1])
            if piece == "--":
                p.draw.rect(screen, p.Color(color), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                return True
            elif piece[0] == "w":
                p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                drawPieces(screen, board)
                return False
        else:
            return False

'''
Same as drawPossibleMoves but it is for the Pawn's special attacks
'''
def drawPossibleMovesP(coordinate, color, screen, board, firstMove):
    global availableMoves
    if coordinate[0] < 0 or coordinate[0] > 7:
        return False
    if coordinate[1] < 0 or coordinate[1] > 7:
        return False
    piece = board[coordinate[0]][coordinate[1]]
    #print("piece " + piece)
    #print("piece's coord " + str(coordinate[0]) + " " + str(coordinate[1]))

    if piece == "--":
        p.draw.rect(screen, p.Color(color), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        availableMoves.append(coordinate[0])
        availableMoves.append(coordinate[1])
    if gs.whiteToMove == True and firstMove == False:
        #check if there is an enemy piece for the white pawn diagnally to attack
        try:
            coordinate[1] += 1
            #print("Diagnal attack " + str(coordinate))
            piece = board[coordinate[0]][coordinate[1]]
            if piece[0] == "b":
                p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                availableMoves.append(coordinate[0])
                availableMoves.append(coordinate[1])
        except:
            pass
        coordinate[1] -= 1
        try:
            coordinate[1] -= 1
            piece = board[coordinate[0]][coordinate[1]]
            if piece[0] == "b":
                p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                availableMoves.append(coordinate[0])
                availableMoves.append(coordinate[1])
        except:
            pass
        coordinate[1] += 1
        #region EnPassant
        #En Passant attack: attack diagnally behind enemy piece to capture it
        # try:
        #     coordinate[0] +=1
        #     coordinate[1] += 1
        #     piece = board[coordinate[0]][coordinate[1]]
        #     coordinate[0] -=1
        #     coordinate[1] -= 1
        #     if piece[0] == "b":
        #         print("here")
        #         coordinate[1] += 1
        #         p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        #         print(coordinate)
        #         availableMoves.append(coordinate[0])
        #         availableMoves.append(coordinate[1])
        #         gs.enPassant = True
        # except:
        #     pass
        # coordinate[1] -= 1
        # print(coordinate)

        # try:
        #     coordinate[0] +=1
        #     coordinate[1] -= 1
        #     piece = board[coordinate[0]][coordinate[1]]
        #     coordinate[0] -=1
        #     coordinate[1] += 1
        #     if piece[0] == "b":
        #         coordinate[1] -= 1
        #         p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        #         availableMoves.append(coordinate[0])
        #         availableMoves.append(coordinate[1])
        #         gs.enPassant = True
        # except:
        #     pass
        # coordinate[1] += 1
        #endregion
        #print("after "+ str(coordinate))
    elif gs.whiteToMove == False:
        #check if there is an enemy piece for the white pawn diagnally to attack
        try:
            coordinate[1] -= 1
            piece = board[coordinate[0]][coordinate[1]]
            if piece[0] == "w":
                p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                availableMoves.append(coordinate[0])
                availableMoves.append(coordinate[1])
        except:
            pass
        coordinate[1] += 1
        try:
            coordinate[1] += 1
            #print(coordinate)
            piece = board[coordinate[0]][coordinate[1]]
            if piece[0] == "w":
                p.draw.rect(screen, p.Color("red"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                availableMoves.append(coordinate[0])
                availableMoves.append(coordinate[1])
        except:
            pass
        coordinate[1] -= 1

    drawPieces(screen, board)

'''
Gets end coordinates for player piece move.
'''
def movePiece(availableMoves, mx, my):
    if gs.whiteToMove == True:
        for r,c in zip(availableMoves[0::2], availableMoves[1::2]):
            if p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE).collidepoint(mx, my): #see if the cursor coords are within the piece's square
                endCoord = [r, c]
                return endCoord
    else:
        #print(availableMoves)
        rand_idx = random.randrange(len(availableMoves))
        #print(rand_idx)
        if rand_idx % 2 != 0:
            c = availableMoves[rand_idx]
            r = availableMoves[rand_idx - 1]
        else:
            c = availableMoves[rand_idx + 1]
            r = availableMoves[rand_idx]
        endCoord = [r, c]
        #print(endCoord)
        return endCoord

'''
After everymover scan the board to see if there is a check
'''
def checkScanner(screen):
    board = gs.board
    #drawPieces(screen, gs.board)
    #selectedCoord[0] = row; selectedCoord[1] = column
    #check if the pawn has already been moved
    #change coordinates to display the possible moves then revert the coordinates for future use
    #print(selectedPiece)
    for r in range(DIMESION):
        for c in range(DIMESION):
            piece = gs.board[r][c]
            selectedCoord = [r, c]
            if piece == "wP":
                selectedCoord[0] -= 1
                drawCheckMovesP(selectedCoord,   screen, gs.board, True)
                selectedCoord[0] += 1
            elif piece == "bP":
                selectedCoord[0] += 1
                drawCheckMovesP(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 1
            elif piece == "wR":
                revert = 0
                keepGoing = True
                while selectedCoord[0] > 0 and keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                    revert += 1       
                    selectedCoord[0] -= 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[0] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[0] += 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= revert

                revert = 0
                keepGoing = True
                while selectedCoord[1] > 0 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] -= 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[1] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[1] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] += 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[1] -= revert

            elif piece == "bR":
                revert = 0
                keepGoing = True
                while selectedCoord[0] > 0 and keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                    revert += 1       
                    selectedCoord[0] -= 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[0] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[0] += 1
                    keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, False)
                selectedCoord[0] -= revert

                revert = 0
                keepGoing = True
                while selectedCoord[1] > 0 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] -= 1
                    keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, False)
                selectedCoord[1] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[1] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] += 1
                    keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, False)
                selectedCoord[1] -= revert

            elif  piece == "wB":
                revert = 0
                keepGoing = True
                if gs.whiteToMove == True:
                    #diagnol up-right
                    try:
                        while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                            revert += 1       
                            selectedCoord[0] -= 1
                            selectedCoord[1] += 1
                            keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, True)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] += revert
                    selectedCoord[1] -= revert

                    revert = 0
                    keepGoing = True
                    #diagnol up-left
                    try:
                        while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                            revert += 1       
                            selectedCoord[0] -= 1
                            selectedCoord[1] -= 1
                            keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, True)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] += revert
                    selectedCoord[1] += revert

                    revert = 0
                    keepGoing = True
                    #diagnol down-right
                    try:
                        while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                            revert += 1       
                            selectedCoord[0] += 1
                            selectedCoord[1] += 1
                            keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, True)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] -= revert
                    selectedCoord[1] -= revert

                    revert = 0
                    keepGoing = True
                    #diagnol down-left
                    try:
                        while keepGoing == True:
                            revert += 1       
                            selectedCoord[0] += 1
                            selectedCoord[1] -= 1
                            keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, True)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] -= revert
                    selectedCoord[1] += revert

            elif  piece == "bB":
                revert = 0
                keepGoing = True
                if gs.whiteToMove == True:
                    #diagnol up-right
                    try:
                        while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                            revert += 1       
                            selectedCoord[0] -= 1
                            selectedCoord[1] += 1
                            keepGoing = drawCheckMoves(selectedCoord, screen, gs.board, False)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] += revert
                    selectedCoord[1] -= revert

                    revert = 0
                    keepGoing = True
                    #diagnol up-left
                    try:
                        while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                            revert += 1       
                            selectedCoord[0] -= 1
                            selectedCoord[1] -= 1
                            keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] += revert
                    selectedCoord[1] += revert

                    revert = 0
                    keepGoing = True
                    #diagnol down-right
                    try:
                        while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                            revert += 1       
                            selectedCoord[0] += 1
                            selectedCoord[1] += 1
                            keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] -= revert
                    selectedCoord[1] -= revert

                    revert = 0
                    keepGoing = True
                    #diagnol down-left
                    try:
                        while keepGoing == True:
                            revert += 1       
                            selectedCoord[0] += 1
                            selectedCoord[1] -= 1
                            keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                    except:
                        pass
                    keepGoing = False
                    selectedCoord[0] -= revert
                    selectedCoord[1] += revert

            elif piece == "wN":
                #diagnol up-right
                selectedCoord[0] -= 2
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += 2
                selectedCoord[1] -= 1

                #diagnol up-left
                selectedCoord[0] -= 2
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += 2
                selectedCoord[1] += 1

                #diagnol down-right 
                selectedCoord[0] += 2
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= 2
                selectedCoord[1] -= 1

                #diagnol down-left
                selectedCoord[0] += 2
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= 2
                selectedCoord[1] += 1

                #diagnol left-up
                selectedCoord[0] += 1
                selectedCoord[1] -= 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= 1
                selectedCoord[1] += 2

                #diagnol left-down
                selectedCoord[0] -= 1
                selectedCoord[1] -= 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += 1
                selectedCoord[1] += 2

                #diagnol right-up
                selectedCoord[0] -= 1
                selectedCoord[1] += 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += 1
                selectedCoord[1] -= 2

                #diagnol right-down
                selectedCoord[0] += 1
                selectedCoord[1] += 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= 1
                selectedCoord[1] -= 2

                #diagnol up-left
                selectedCoord[0] += 1
                selectedCoord[1] -= 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= 1
                selectedCoord[1] += 2

            elif piece == "bN":
                #diagnol up-right
                selectedCoord[0] -= 2
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += 2
                selectedCoord[1] -= 1

                #diagnol up-left
                selectedCoord[0] -= 2
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += 2
                selectedCoord[1] += 1

                #diagnol down-right 
                selectedCoord[0] += 2
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 2
                selectedCoord[1] -= 1

                #diagnol down-left
                selectedCoord[0] += 2
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 2
                selectedCoord[1] += 1

                #diagnol left-up
                selectedCoord[0] += 1
                selectedCoord[1] -= 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 1
                selectedCoord[1] += 2

                #diagnol left-down
                selectedCoord[0] -= 1
                selectedCoord[1] -= 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += 1
                selectedCoord[1] += 2

                #diagnol right-up
                selectedCoord[0] -= 1
                selectedCoord[1] += 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += 1
                selectedCoord[1] -= 2

                #diagnol right-down
                selectedCoord[0] += 1
                selectedCoord[1] += 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 1
                selectedCoord[1] -= 2

                #diagnol up-left
                selectedCoord[0] += 1
                selectedCoord[1] -= 2
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 1
                selectedCoord[1] += 2

            elif piece == "wQ":
                #Rook attributes
                revert = 0
                keepGoing = True
                while selectedCoord[0] > 0 and keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                    revert += 1       
                    selectedCoord[0] -= 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[0] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[0] += 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= revert

                revert = 0
                keepGoing = True
                while selectedCoord[1] > 0 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] -= 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[1] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[1] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] += 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[1] -= revert

                #Bishop attributes
                revert = 0
                keepGoing = True
                #diagnol up-right
                try:
                    while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                        revert += 1       
                        selectedCoord[0] -= 1
                        selectedCoord[1] += 1
                        keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] += revert
                selectedCoord[1] -= revert

                revert = 0
                keepGoing = True
                #diagnol up-left
                try:
                    while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                        revert += 1       
                        selectedCoord[0] -= 1
                        selectedCoord[1] -= 1
                        keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] += revert
                selectedCoord[1] += revert

                revert = 0
                keepGoing = True
                #diagnol down-right
                try:
                    while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                        revert += 1       
                        selectedCoord[0] += 1
                        selectedCoord[1] += 1
                        keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] -= revert
                selectedCoord[1] -= revert

                revert = 0
                keepGoing = True
                #diagnol down-left
                try:
                    while keepGoing == True:
                        revert += 1       
                        selectedCoord[0] += 1
                        selectedCoord[1] -= 1
                        keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, True)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] -= revert
                selectedCoord[1] += revert

                #Diagnol Moves
                selectedCoord[0] -= 1
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += 1
                selectedCoord[1] += 1
                selectedCoord[0] += 1
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= 1
                selectedCoord[1] -= 1
                selectedCoord[0] += 1
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] -= 1
                selectedCoord[1] += 1
                selectedCoord[0] -= 1
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, True)
                selectedCoord[0] += 1
                selectedCoord[1] -= 1

            elif piece == "bQ":
                #Rook attributes
                revert = 0
                keepGoing = True
                while selectedCoord[0] > 0 and keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                    revert += 1       
                    selectedCoord[0] -= 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[0] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[0] += 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= revert

                revert = 0
                keepGoing = True
                while selectedCoord[1] > 0 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] -= 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[1] += revert

                keepGoing = True
                revert = 0
                while selectedCoord[1] < 7 and keepGoing == True:
                    revert += 1       
                    selectedCoord[1] += 1
                    keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[1] -= revert

                #Bishop attributes
                revert = 0
                keepGoing = True
                #diagnol up-right
                try:
                    while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                        revert += 1       
                        selectedCoord[0] -= 1
                        selectedCoord[1] += 1
                        keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] += revert
                selectedCoord[1] -= revert

                revert = 0
                keepGoing = True
                #diagnol up-left
                try:
                    while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                        revert += 1       
                        selectedCoord[0] -= 1
                        selectedCoord[1] -= 1
                        keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] += revert
                selectedCoord[1] += revert

                revert = 0
                keepGoing = True
                #diagnol down-right
                try:
                    while keepGoing == True: # get all the available moves up untill a piece blocking the path or the edge of the board
                        revert += 1       
                        selectedCoord[0] += 1
                        selectedCoord[1] += 1
                        keepGoing = drawCheckMoves(selectedCoord  , screen, gs.board, False)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] -= revert
                selectedCoord[1] -= revert

                revert = 0
                keepGoing = True
                #diagnol down-left
                try:
                    while keepGoing == True:
                        revert += 1       
                        selectedCoord[0] += 1
                        selectedCoord[1] -= 1
                        keepGoing = drawCheckMoves(selectedCoord , screen, gs.board, False)
                except:
                    pass
                keepGoing = False
                selectedCoord[0] -= revert
                selectedCoord[1] += revert

                #Diagnol Moves
                selectedCoord[0] -= 1
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += 1
                selectedCoord[1] += 1
                selectedCoord[0] += 1
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 1
                selectedCoord[1] -= 1
                selectedCoord[0] += 1
                selectedCoord[1] -= 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] -= 1
                selectedCoord[1] += 1
                selectedCoord[0] -= 1
                selectedCoord[1] += 1
                if selectedCoord[0] >= 0 and selectedCoord[0] <=7 and selectedCoord[1] >= 0 and selectedCoord[1] <=7:
                    drawCheckMoves(selectedCoord  , screen, gs.board, False)
                selectedCoord[0] += 1
                selectedCoord[1] -= 1
'''
Checks the possible moves for the piece to see if it checks the king
'''
def drawCheckMovesP(coordinate, screen, board, isWhite):
    if coordinate[0] < 0 or coordinate[0] > 7:
        return False
    if coordinate[1] < 0 or coordinate[1] > 7:
        return False
    piece = board[coordinate[0]][coordinate[1]]
    #print("piece " + piece)
    #print("piece's coord " + str(coordinate[0]) + " " + str(coordinate[1]))
    if isWhite:
        #check if there is an enemy piece for the white pawn diagnally to attack
        try:
            coordinate[1] += 1
            #print("Diagnal attack " + str(coordinate))
            piece = board[coordinate[0]][coordinate[1]]
            if piece == "bK":
                p.draw.rect(screen, p.Color("purple"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                check()
        except:
            pass
        coordinate[1] -= 1
        try:
            coordinate[1] -= 1
            piece = board[coordinate[0]][coordinate[1]]
            if piece == "bK":
                p.draw.rect(screen, p.Color("purple"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                check()
        except:
            pass
        coordinate[1] += 1

            #print("after "+ str(coordinate))
    elif isWhite == False:
        #check if there is an enemy piece for the white pawn diagnally to attack
        try:
            coordinate[1] -= 1
            piece = board[coordinate[0]][coordinate[1]]
            if piece == "wK":
                p.draw.rect(screen, p.Color("purple"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                check()
        except:
            pass
        coordinate[1] += 1
        try:
            coordinate[1] += 1
            #print(coordinate)
            piece = board[coordinate[0]][coordinate[1]]
            if piece == "wK":
                p.draw.rect(screen, p.Color("purple"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                check()
        except:
            pass
        coordinate[1] -= 1

    drawPieces(screen, board)

def drawCheckMoves(coordinate, screen, board, isWhite):
    if coordinate[0] < 0 or coordinate[0] > 7:
        return False
    if coordinate[1] < 0 or coordinate[1] > 7:
        return False
    piece = board[coordinate[0]][coordinate[1]]
    if isWhite: #The function is called after white has already moved, but black hasn't moved yet. Scan for check on black king
        if piece == "bK":
            p.draw.rect(screen, p.Color("purple"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            check()
    elif isWhite == False:
        if piece == "wK":
            p.draw.rect(screen, p.Color("purple"), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            check()

'''
Called when the king is in check. Used for the logic behind getting out of check.
'''
def check():
    print("check")


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
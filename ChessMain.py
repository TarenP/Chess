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
wP0 = True
wP1 = True
wP2 = True
wP3 = True
wP4 = True
wP5 = True
wP6 = True
wP7 = True


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
    alrSelected = False #Once a piece is selected, it has to be moved.
    drawGameState(screen, gs)
    while running:
        for e in p.event.get():
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1 and alrSelected == False:
                    alrSelected = True
                    #print(mx)
                    #print(my)
                    selectedCoord, selectedPiece = selectPiece(mx, my, gs.board, screen)
                    print(selectedCoord)
                    possibleMoves(selectedCoord, gs, screen, selectedPiece)
                else:
                    endCoord = movePiece(availableMoves, mx, my, gs.board, screen)
                    if endCoord == None:
                        break
                    print(selectedCoord)
                    print(endCoord)
                    move = ChessEngine.Move(selectedCoord, endCoord, gs.board)
                    #print(gs.moveLog)
                    gs.makeMove(move)
                    #print(gs.board)
                    drawGameState(screen, gs)
                    alrSelected = False

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
                selectedCoord = [-1, -1]
                #print(selected) 
    return selectedCoord, piece

'''
Logic for possible moves for each piece depending on piece type
'''
def possibleMoves(selectedCoord, gs, screen, selectedPiece):
    board = gs.board

    global wP0, wP1,wP2,wP3,wP4,wP5,wP6,wP7, availableMoves

    availableMoves = []
    #drawPieces(screen, gs.board)
    #selectedCoord[0] = row; selectedCoord[1] = column
    #check if the pawn has already been moved
    #change coordinates to display the possible moves then revert the coordinates for future use
    print(selectedPiece)
    if selectedPiece[1] == "P":
        if ('wP' + str(selectedCoord[1])) == "wP0":
            if wP0 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP0 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] -= 1
        elif ('wP' + str(selectedCoord[1])) == "wP1":
            if wP1 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP1 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
        elif ('wP' + str(selectedCoord[1])) == "wP2":
            if wP2 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP2 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
        elif ('wP' + str(selectedCoord[1])) == "wP3":
            if wP3 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP3 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
        elif ('wP' + str(selectedCoord[1])) == "wP4":
            if wP4 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP4 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
        elif ('wP' + str(selectedCoord[1])) == "wP5":
            if wP5 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP5 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
        elif ('wP' + str(selectedCoord[1])) == "wP6":
            if wP6 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP6 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
        elif ('wP' + str(selectedCoord[1])) == "wP7":
            if wP7 == True:
                selectedCoord[0] -= 2
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 2
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
                wP7 = False
            else:
                selectedCoord[0] -= 1
                drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
                selectedCoord[0] += 1
    
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
            print(revert)
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
            print(revert)
            selectedCoord[1] += 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        selectedCoord[1] -= revert

    elif  selectedPiece[1] == "B":
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

    elif selectedPiece[1] == "N":
        #diagnol up-right
        try:  
            selectedCoord[0] -= 2
            selectedCoord[1] += 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
            selectedCoord[0] += 2
            selectedCoord[1] -= 1
        except:
            pass

        #diagnol up-left
        try:  
            selectedCoord[0] -= 2
            selectedCoord[1] -= 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
            selectedCoord[0] += 2
            selectedCoord[1] += 1
        except:
            pass

        #diagnol down-right
        try:  
            selectedCoord[0] += 2
            selectedCoord[1] += 1
            keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
            selectedCoord[0] -= 2
            selectedCoord[1] -= 1
        except:
            pass

        # #diagnol down-left
        # try:  
        #     selectedCoord[0] += 2
        #     selectedCoord[1] -= 1
        #     keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        #     selectedCoord[0] -= 2
        #     selectedCoord[1] += 1
        # except:
        #     pass

        # #diagnol left-up
        # try:  
        #     selectedCoord[0] += 1
        #     selectedCoord[1] -= 2
        #     keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        #     selectedCoord[0] -= 1
        #     selectedCoord[1] += 2
        # except:
        #     pass

        # #diagnol left-down
        # try:  
        #     selectedCoord[0] -= 1
        #     selectedCoord[1] -= 2
        #     keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        #     selectedCoord[0] += 2
        #     selectedCoord[1] += 1
        # except:
        #     pass

        # #diagnol right-up
        # try:  
        #     selectedCoord[0] -= 1
        #     selectedCoord[1] += 2
        #     keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        #     selectedCoord[0] += 1
        #     selectedCoord[1] -= 2
        # except:
        #     pass

        # #diagnol up-left
        # try:  
        #     selectedCoord[0] += 1
        #     selectedCoord[1] -= 2
        #     keepGoing = drawPossibleMoves(selectedCoord, "cadetblue2", screen, gs.board)
        #     selectedCoord[0] -= 1
        #     selectedCoord[1] += 2
        # except:
        #     pass
'''
Draw the possible moves. Used by possibleMoves to create a visual of the possible moves.
Choice for color so I can easily change it so the ending spot for each possible move is a different color than the path
Checks if another piece is blocking the path
'''
def drawPossibleMoves(coordinate, color, screen, board):
    global availableMoves
    piece = board[coordinate[0]][coordinate[1]]
    availableMoves.append(coordinate[0])
    availableMoves.append(coordinate[1])
    if piece == "--":
        p.draw.rect(screen, p.Color(color), p.Rect(coordinate[1]*SQ_SIZE, coordinate[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        return True
    else:
        return False

'''
Gets end coordinates for piece move.
'''
def movePiece(availableMoves, mx, my, board, screen):
    for r,c in zip(availableMoves[0::2], availableMoves[1::2]):
        selectedMove = board[r][c] #Get name of piece
        if p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE).collidepoint(mx, my): #see if the cursor coords are within the piece's square
            endCoord = [r, c]
            return endCoord

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
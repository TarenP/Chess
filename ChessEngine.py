"""
This class is responsible for storing all the information about the current state of the chess game. It will also be responsible for determining the valid moves
at the current state. It will also keep a move log.
"""
class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element has 2 characters.
        #The first character represents the color of the piece, 'b' or 'w'
        #The second character represents the type of piece, 'K', 'Q', 'R', 'B', 'N', or 'P'
        #"--" represents and empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "--", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bK", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.resetPiece = False#used to tell if we need to reset a move
        # self.enPassant = False
        #keep track of if a pawn has moved from its starting position for 2 forward move
        self.moveLog = []
        self.whiteCapturedLog = []#Keep track of the white pieces that are captured
        self.blackCapturedLog = []#Keep track of the black pieces that are captured

    def makeMove(self, move):
        # if self.whiteToMove == True:
        #     self.blackCapturedLog.append(self.board[move.endRow][move.endCol])
        # else:
        #     self.whiteCapturedLog.append(self.board[move.endRow][move.endCol])
        if self.resetPiece:
            self.board[move.startRow][move.startCol] = self.storePiece
            print(self.storePiece)
            self.board[move.endRow][move.endCol] = move.pieceMoved
        else:
            self.storePiece = self.board[move.endRow][move.endCol] #stores the piece so the move can be undone
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.pieceMoved
            print(move.endRow)
            print(move.endCol)

        # if self.enPassant == True:
        #     self.board[move.endRow - 1][move.endCol] = "--"
        self.moveLog.append(move)#log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove #swap players
        self.enPassant = False

class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        print(self.endRow)
        print(self.endCol)
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
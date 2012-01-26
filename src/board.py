'''
board.py:
This module defines class Board, which controls the game logic.
'''

import random, os
from config import *
from ctypes import *

class Board:

    def __init__(self):
        
        # the game board is represented as a 2-dimension array.
        self.board = [ [0,0,0,0,0,0,0,0], \
                       [0,0,0,0,0,0,0,0], \
                       [0,0,0,0,0,0,0,0], \
                       [0,0,0,2,1,0,0,0], \
                       [0,0,0,1,2,0,0,0], \
                       [0,0,0,0,0,0,0,0], \
                       [0,0,0,0,0,0,0,0], \
                       [0,0,0,0,0,0,0,0] ]
        
        #import the C extension which implement the AI of the game.
        self.minimax = cdll.LoadLibrary(os.getcwd() + '/minimax.so')

        # open the file opening.txt and use its content to initialize the open book dictionary openDict.
        d1 = {}
        fp = open('openings.txt', 'r')
        for line in fp:
            i, d2, line = 0, d1, line.rstrip('\n\r')
            while i < len(line):
                key = line[i] + line[i+1]
                if key in d2.keys():
                    d2 = d2[key]
                else:
                    d2[key] = self.str2dict(line[i+2:])
                    break
                i += 2
        fp.close()
        self.openDict = {}
        self.openDict['a1'] = d1

    # return a player's all the avlible moves for a given position.
    def getAvlbMoves(self, color):
        unColor, moves = 3 - color, []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    #Search in the up direction
                    if i > 1:
                        k = 1
                        while i-k>=0 and self.board[i-k][j]==unColor:
                            k += 1
                        if k>1 and i-k>=0 and self.board[i-k][j]==0:
                            moves.append((i-k,j))
                    #Search in the down direction
                    if i < 6:
                        k = 1
                        while i+k<=7 and self.board[i+k][j]==unColor:
                            k += 1
                        if k>1 and i+k<=7 and self.board[i+k][j]==0:
                            moves.append((i+k,j))
                    #Search in the left direction
                    if j > 1:
                        k = 1
                        while j-k>=0 and self.board[i][j-k]==unColor:
                            k += 1
                        if k>1 and j-k>=0 and self.board[i][j-k]==0:
                            moves.append((i,j-k))
                    #Search in the right direction
                    if j < 6:
                        k = 1
                        while j+k<=7 and self.board[i][j+k]==unColor:
                            k += 1
                        if k>1 and j+k<=7 and self.board[i][j+k]==0:
                            moves.append((i,j+k))
                    #Search in the northwest direction
                    if i > 1 and j > 1:
                        k = 1
                        while i-k>=0 and j-k>=0 and self.board[i-k][j-k]==unColor:
                            k += 1
                        if k>1 and i-k>=0 and j-k>=0 and self.board[i-k][j-k]==0:
                            moves.append((i-k,j-k))
                    #Search in the northeast direction
                    if i > 1 and j < 6:
                        k = 1
                        while i-k>=0 and j+k<=7 and self.board[i-k][j+k]==unColor:
                            k += 1
                        if k>1 and i-k>=0 and j+k<=7 and self.board[i-k][j+k]==0:
                            moves.append((i-k,j+k))
                    #Search in the southwest direction
                    if i < 6 and j > 1:
                        k = 1
                        while i+k<=7 and j-k>=0 and self.board[i+k][j-k]==unColor:
                            k += 1
                        if k>1 and i+k<=7 and j-k>=0 and self.board[i+k][j-k]==0:
                            moves.append((i+k,j-k))
                    #Search in the southeast direction
                    if i < 6 and j < 6:
                        k = 1
                        while i+k<=7 and j+k<=7 and self.board[i+k][j+k]==unColor:
                            k += 1
                        if k>1 and i+k<=7 and j+k<=7 and self.board[i+k][j+k]==0:
                            moves.append((i+k,j+k))
        return list(set(moves))

    # print the board. just for debug.
    def printBoard(self):
        for i in range(8):
            print self.board[i]

    # check if the board is full, used to check if the game is over.
    def isFull(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == BLANK:
                    return False
        return True 
    
    # return the number of black, white and empty of the board
    def countBoard(self): 
        b = w = e = 0   
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == BLACK:
                    b += 1
                elif self.board[i][j] == WHITE:
                    w += 1
                else:
                    e += 1
        return b, w, e

    # Update the board after a move at (row,col).Return all the influnced positions.
    def update(self, row, col, color):
        unColor, updated = 3-color, [(row,col)]
        self.board[row][col] = color
        #Search in the up direction
        if row > 1:
            k = 1
            while row-k>=0 and self.board[row-k][col]==unColor:
                k += 1
            if k>1 and row-k>=0 and self.board[row-k][col]==color:
                for p in range(1,k):
                    self.board[row-p][col] = color
                    updated.append((row-p, col))

        #Search in the down direction
        if row < 6:
            k = 1
        while row+k<=7 and self.board[row+k][col]==unColor:
            k += 1
        if k>1 and row+k<=7 and self.board[row+k][col]==color:
            for p in range(1,k):
                self.board[row+p][col] = color
                updated.append((row+p, col))

        #Search in the left direction
        if col > 1:
            k = 1
        while col-k>=0 and self.board[row][col-k]==unColor:
            k += 1
        if k>1 and col-k>=0 and self.board[row][col-k]==color:
            for p in range(1, k):
                self.board[row][col-p] = color
                updated.append((row, col-p))

        #Search in the right direction
        if col < 6:
            k = 1
        while col+k<=7 and self.board[row][col+k]==unColor:
            k += 1
        if k>1 and col+k<=7 and self.board[row][col+k]==color:
            for p in range(1, k):
                self.board[row][col+p] = color
                updated.append((row,col+p))

        #Search in the northwest direction
        if row > 1 and col > 1:
            k = 1
        while row-k>=0 and col-k>=0 and self.board[row-k][col-k]==unColor:
            k += 1
        if k>1 and row-k>=0 and col-k>=0 and self.board[row-k][col-k]==color:
            for p in range(1, k):
                self.board[row-p][col-p] = color
                updated.append((row-p,col-p))

        #Search in the northeast direction
        if row > 1 and col < 6:
            k = 1
        while row-k>=0 and col+k<=7 and self.board[row-k][col+k]==unColor:
            k += 1
        if k>1 and row-k>=0 and col+k<=7 and self.board[row-k][col+k]==color:
            for p in range(1, k):
                self.board[row-p][col+p] = color
                updated.append((row-p,col+p))

        #Search in the southwest direction
        if row < 6 and col > 1:
            k = 1
        while row+k<=7 and col-k>=0 and self.board[row+k][col-k]==unColor:
            k += 1
        if k>1 and row+k<=7 and col-k>=0 and self.board[row+k][col-k]==color:
            for p in range(1, k):
                self.board[row+p][col-p] = color
                updated.append((row+p,col-p))

        #Search in the southeast direction
        if row < 6 and col < 6:
            k = 1
        while row+k<=7 and col+k<=7 and self.board[row+k][col+k]==unColor:
            k += 1
        if k>1 and row+k<=7 and col+k<=7 and self.board[row+k][col+k]==color:
            for p in range(1, k):
                self.board[row+p][col+p] = color
                updated.append((row+p,col+p))

        return updated

    # get a move from AI
    def getFromCmptr(self, color):
        ''''
        avlbMoves = self.getAvlbMoves(color)
        if len(avlbMoves) == 0:
            return None, None
        elif len(avlbMoves) == 1:
            return avlbMoves[0]
        return avlbMoves[random.randint(0, len(avlbMoves)-1)]
        '''
        oneDBoard = (c_char * 64) ()
        for i in range(64):
            oneDBoard[i] = chr(self.board[i/8][i%8])
        rc = self.minimax.giveNextMove(oneDBoard, color)
        if rc == -1:
            return None, None
        print (rc/10, rc%10)
        return (rc/10, rc%10)

    def str2dict(self, strr):
        if not strr:
            return None
        d = {}
        length = len(strr)-1
        i = length
        while i > 0:
            key = strr[i-1]+strr[i]
            if i == length:
                d[key] = None
            else:
                d2 = d.copy()
                d = {}
                d[key] = d2
            i -= 2
        return d

    def getFromOpenBook(self, lastMove):
            try:
                self.openDict = self.openDict[lastMove]
                length = len(self.openDict.keys())
                r = random.randint(0, length-1)
                if random.randint(0, 13) == 5:
                    r = random.randint(0, length-1)
                best_move = self.openDict.keys()[r]
                self.openDict = self.openDict[best_move]
                return (int(best_move[1])-1, ord(best_move[0])-97)
            except:
                return (None, None)

'''
gcc -c -fPIC minimax.c
gcc -shared minimax.o -o minimax.so
'''


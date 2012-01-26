'''
gui.py
This module defines class Gui, which shows the game board and controls all the interaction with the user.
'''

import pygame, sys
from pygame.locals import *
from config import *

class Gui:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((798,540), 0, 32)

        # The Font Object
        self.gamefont = pygame.font.SysFont("arial",16)

        # Get image files
        self.menuBGimg = pygame.image.load("images/menuBG.png").convert()
        self.waitingConnectImg = pygame.image.load("images/waitingConnect.png").convert_alpha()
        self.enterIPImg = pygame.image.load("images/enterIP.png").convert_alpha()
        self.bgimg = pygame.image.load("images/bg.png").convert()
        self.bchessimg = pygame.image.load("images/bchess.png").convert_alpha()
        self.wchessimg = pygame.image.load("images/wchess.png").convert_alpha()
        self.pointerImg = pygame.image.load("images/pointer.png").convert_alpha()
        self.avlimg = pygame.image.load("images/avl.png").convert_alpha()
        self.gridimg = pygame.image.load("images/grid.png").convert_alpha()
        self.dialogBGimg = pygame.image.load("images/dialogBG.png").convert_alpha()
        self.okButtonImg = pygame.image.load("images/okButton.png").convert_alpha()

    def showBoard(self, p1, p2):
        self.screen.blit(self.bgimg, (0,0))
        self.gamefont = pygame.font.SysFont("arial", 30)
        self.screen.blit(self.gamefont.render(p1, True, (0,0,0)), (555,125))
        self.screen.blit(self.gamefont.render(p2, True, (255,255,255)), (555,295))
        self.screen.blit(self.wchessimg, (210,210))
        self.screen.blit(self.bchessimg, (270,210))
        self.screen.blit(self.bchessimg, (210,270))
        self.screen.blit(self.wchessimg, (270,270))

        pygame.display.update()


    def showMainMenu(self):
        self.screen.blit(self.menuBGimg, (0,0))
        pygame.display.update()

    def getOption(self):
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and 230<event.pos[0]<590:
                    if 105<event.pos[1]<145:
                        return 1
                    elif 160<event.pos[1]<200:
                        return 2
                    elif 220<event.pos[1]<265:
                        return 3
                    elif 285<event.pos[1]<325:
                        return 4
                    elif 345<event.pos[1]<385:
                        return 5
                    elif 405<event.pos[1]<450:
                        return 6
                    elif 465<event.pos[1]<505:
                        sys.exit()

    def showIP(self):
        self.screen.blit(self.waitingConnectImg, (220,155))
        self.gamefont = pygame.font.SysFont("arial",20)
        self.screen.blit(self.gamefont.render("Your IP is "+"127.0.0.1", True, (255,255,255)), (250,170))
        self.screen.blit(self.gamefont.render("Please tell it to your friend", True, (255,255,255)), (250,200))
        self.screen.blit(self.gamefont.render("Waiting for Connect ... ... ...", True, (255,255,255)), (250,230))
        pygame.display.update()

    def getCancel(self, s, g):
        i = 0
        while True:
            event = pygame.event.wait()
            if i == 0:
                i = 1
                continue
            if event.type == MOUSEBUTTONUP and event.button == 1:
                s.close()
                g.restart()
                return

    def getServerIP(self):
        ip = ''
        self.gamefont = pygame.font.SysFont("arial",20)
        self.screen.blit(self.enterIPImg, (220,155))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if ('0' <= event.unicode <= '9' or event.unicode == '.') and len(ip)<15:
                        ip += event.unicode
                    elif event.key == K_BACKSPACE:
                        ip = ip[:-1]
                    elif event.key == K_RETURN:
                        return ip
                    self.screen.blit(self.enterIPImg, (220,155))
                    self.screen.blit(self.gamefont.render(ip, True, (255,255,255)), (250,233))
                    pygame.display.update()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and 290<event.pos[1]<324:
                    if 245<event.pos[0]<390:
                        return ip
                    elif 420<event.pos[0]<570:
                        return 'cancel'

    def getInput(self, avlbMoves):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if 553<event.pos[0]<757 and 469<event.pos[1]<504:
                        return -1, -1
                    col, row = (event.pos[0]-EDGEWIDTH)/GRIDWIDTH, (event.pos[1]-EDGEWIDTH)/GRIDWIDTH
                    if (row, col) in avlbMoves:
                        return row, col

    def showPassInfo(self, color):
        self.showDialog(('BLACK' if color==BLACK else 'WHITE')+" Has No Move, Pass Needed")

    def putChess(self, updated, color):
        if color == WHITE:
            for pos in updated:
                self.screen.blit(self.wchessimg, (pos[1]*GRIDWIDTH+EDGEWIDTH, pos[0]*GRIDWIDTH+EDGEWIDTH))
        elif color == BLACK:
            for pos in updated:
                self.screen.blit(self.bchessimg, (pos[1]*GRIDWIDTH+EDGEWIDTH, pos[0]*GRIDWIDTH+EDGEWIDTH))
        pygame.display.update()
        
    def setCount(self, b, w, e):
        self.screen.blit(self.gridimg, (640, 185))
        self.screen.blit(self.gridimg, (640, 368))
        self.gamefont = pygame.font.SysFont("arial",30)
        self.screen.blit(self.gamefont.render(str(b), True, (255,255,255)), (650, 187))
        self.screen.blit(self.gamefont.render(str(w), True, (0,0,0)), (650, 370))
        pygame.display.update()
    
    def setPointer(self, color):
        if color == BLACK:
            self.screen.blit(self.gridimg, (710, 370))
            self.screen.blit(self.pointerImg, (730, 190))
        else:
            self.screen.blit(self.gridimg, (710, 180))
            self.screen.blit(self.pointerImg, (730, 375))            
        pygame.display.update()

    def showAvlbMoves(self, avlbMoves):
        for pos in avlbMoves:
            self.screen.blit(self.avlimg, (pos[1]*GRIDWIDTH+EDGEWIDTH, pos[0]*GRIDWIDTH+EDGEWIDTH))
        pygame.display.update()

    def clearAvlbMoves(self, avlbMoves):
        for pos in avlbMoves:
            self.screen.blit(self.gridimg, (pos[1]*GRIDWIDTH+EDGEWIDTH, pos[0]*GRIDWIDTH+EDGEWIDTH))
        pygame.display.update()

    def showWinner(self, BNum, WNum):
        if BNum == WNum:
            self.showDialog("BLACK And WHITE Draw By %d - %d" % (BNum, WNum))
        else:
            self.showDialog(('BLACK' if BNum>WNum else 'WHITE')+" Wins By %d - %d" % (max(BNum,WNum), min(BNum,WNum)))

    def showDialog(self, text):
        self.gamefont = pygame.font.SysFont("arial",16)
        bgBuffer = pygame.image.tostring(self.screen, 'RGBA')
        self.screen.blit(self.dialogBGimg, (90, 150))
        self.screen.blit(self.gamefont.render(text, True, (255,255,255)), (115+(300-self.gamefont.size(text)[0])/2, 200))
        self.screen.blit(self.okButtonImg, (220, 250))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and 220<event.pos[0]<320 and 250<event.pos[1]<277 or event.type == KEYUP and event.key == K_RETURN:
                    self.screen.blit(pygame.image.frombuffer(bgBuffer, (798,540), 'RGBA'), (0,0))
                    pygame.display.update()
                    return


if __name__ == '__main__':
    gui = Gui()
    gui.showBoard('Human(Server)', 'Computer')
    gui.setCount(12, 12, 12)
    gui.setPointer(BLACK)
    gui.setPointer(WHITE)
    raw_input()
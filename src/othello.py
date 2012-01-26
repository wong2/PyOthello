'''
*** stack smashing detected ***: /usr/bin/python terminated
'''

from board import *
from gui import *
from config import *
import player, network, threading

class Othello:

    def __init__(self):
        self.board = Board()
        self.gui = Gui()
        self.useOpenBook = True        

    def choose(self):
        self.gui.showMainMenu()
        option = self.gui.getOption()
        if option == 1:
            self.player1 = player.Computer(BLACK)
            self.player2 = player.Human(WHITE)
            self.run()
        elif option == 2:
            self.player1 = player.Human(BLACK)
            self.player2 = player.Computer(WHITE)
            self.run()
        elif option == 3:
            self.player1 = player.Human(BLACK)
            self.player2 = player.Human(WHITE)
            self.run()
        elif option == 4:
            self.player1 = player.Computer(BLACK)
            self.player2 = player.Computer(WHITE)
            self.run()
        elif option == 5:
            self.gui.showIP()
            self.player1 = player.Human(BLACK)
            self.player2 = player.HumanC(WHITE)
            #t = threading.Thread(target = self.gui.getCancel(self.player2.server.socket, self), name="Child Thread")
            #t.setDaemon(1)
            #t.start()
            self.player2.waitingForClient()
            self.run()
        elif option == 6:
            ip = self.gui.getServerIP()
            if ip == 'cancel':
                self.choose()
                return
            self.player1 = player.HumanS(BLACK, ip)
            self.player2 = player.Human(WHITE)
            self.run()

    def run(self):
        self.gui.showBoard(self.player1.type, self.player2.type)
        player1NoMove, player2NoMoven, n, row, col = False, False, 0, 0, 0
        self.player1.setGuiAndBoard(self.gui, self.board)
        self.player2.setGuiAndBoard(self.gui, self.board)

        while True:
            if player1NoMove and player2NoMove or self.board.isFull():
                blackN, whiteN, EmptyN = self.board.countBoard()
                self.gui.showWinner(blackN, whiteN)
                self.restart()
                return
            self.gui.setPointer(BLACK)
            row, col = self.player1.getNextMove(row, col)
            if row == -1 and col == -1:
                self.restart()
                return
            elif row != None and col != None:
                player1NoMove = False
                updated = self.board.update(row, col, self.player1.color)
                self.gui.putChess(updated, self.player1.color)
                b, w, e = self.board.countBoard()
                self.gui.setCount(b, w, e)
            else:
                player1NoMove = True
                
            self.gui.setPointer(WHITE)
            row, col = self.player2.getNextMove(row, col)
            if row == -1 and col == -1:
                self.restart()
                return                      
            elif row != None and col != None:
                player2NoMove = False
                updated = self.board.update(row, col, self.player2.color)
                self.gui.putChess(updated, self.player2.color)
                b, w, e = self.board.countBoard()
                self.gui.setCount(b, w, e)                  
            else:
                player2NoMove = True
            if self.player1.type == 'Human(Server)':
                self.player1.sendToSvr(row, col)
        
    def restart(self):
        self.board = Board()
        self.gui = Gui()
        self.useOpenBook = True        
        self.choose()
        
if __name__ == '__main__':
    othello = Othello()
    othello.choose()
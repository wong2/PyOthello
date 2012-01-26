'''
network.py
This module defines class Server and Client. They are used in network games.
'''

import socket, sys, os

class Server:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 5543
        self.socket.bind(('', port))
        self.socket.listen(1)

    def waitingForClient(self):
        (self.conn, addr) = self.socket.accept()
        self.cf = self.conn.makefile('rw', 0)
        return str(addr)

    def sendAndGet(self, row, col):
        self.cf.write(str((row, col))+'\n')
        x, y = eval(self.cf.readline()[:-1])
        return (x, y)


    def close(self):
        print "I'm server, Bye!"
        self.conn.close()


class Client:

    def __init__(self, host):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 5543
        self.s.connect((host, port))
        print 'connected to ' + host
        self.sf = self.s.makefile('rw', 0)

    def getFromServer(self):
        row, col = eval(self.sf.readline()[:-1])
        return (row, col)

    def sendToServer(self, row, col):
        self.sf.write(str((row, col))+'\n')

    def close(self):
        self.sf.close()
        self.s.close()
        print "I'm client, bye!"
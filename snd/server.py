import socket
import pickle
import time

class Server():
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8080
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.players = {}
    
    def startServer(self):
        self.server.bind((self.host, self.port))
        while True:
            c, addr = self.server.recvfrom(1024) # recv a data, c == message and addr ip and port
            data = pickle.loads(c)
            if data != None:
                self.players[addr] = {"name":data[0], "pos":data[1]}
            data = pickle.dumps(self.players)
            self.server.sendto(data, addr)

if __name__ == "__main__":
    server = Server()
    server.startServer()
server.server.close()
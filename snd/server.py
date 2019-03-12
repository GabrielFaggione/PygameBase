import socket
import pickle

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
            #if c not in self.players:
            #    self.players[c] = addr
            #    print ("New player online - name",c,", addr",addr)
            #elif c in self.players:
            data = pickle.loads(c)
            print (data)
            print (self.players)
            self.server.sendto(b'Oie', addr)



if __name__ == "__main__":
    server = Server()
    server.startServer()
server.server.close()
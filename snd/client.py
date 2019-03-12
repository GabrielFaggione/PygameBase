import socket
import pickle

class Client():
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = "127.0.0.1"
        self.port = 8080
        self.address = (self.host, self.port)
        self.info = [name, 100, 100]
        self.backinfo = None
    
    def startClient(self):
        self.client.connect(self.address)
        while True:
            try:
                data = pickle.dumps(self.info) # transform info to bytes
                self.client.sendto(data, self.address) # send information to serv
                self.backinfo = self.client.recv(1024) # recv information from serv
                self.info[1] += 1
            except socket.timeout:
                print ("Sem comunicação com o servidor")
                break
        self.client.close()

client = Client("Roberto")
client.startClient()


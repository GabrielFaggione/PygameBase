import socket
import pickle
import queue

class Client():
    def __init__(self, queue):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = "127.0.0.1"
        self.port = 8080
        self.address = (self.host, self.port)
        #self.info = [name, 100, 100]
        self.info = None
        self.backinfo = None
        self.q = queue
    
    def startClient(self):
        self.client.connect(self.address)
        while True:
            try:
                if not self.q["game"].empty():
                    self.info = self.q["game"].get()
                data = pickle.dumps(self.info) # transform info to bytes
                self.client.sendto(data, self.address) # send information to serv
                self.backinfo = self.client.recv(1024) # recv information from serv
                self.q["client"].put(self.backinfo)
            except socket.timeout:
                print ("Sem comunicação com o servidor")
                break
        self.client.close()

#client = Client("Roberto")
#client.startClient()


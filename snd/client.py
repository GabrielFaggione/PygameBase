import socket
import pickle



client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "127.0.0.1"
port = 8080

info = pickle.dumps(["Josué", 100, 100])

client.connect((host, port))
client.sendto(info, (host, port))
print (client.recv(1024))


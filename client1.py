import socket
import json

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
#
# ClientSocket.send(str.encode(Input))
while True:
    Response = ClientSocket.recv(1024)
    data = Response.decode('utf-8');
    y = json.loads(data)
    print(y)

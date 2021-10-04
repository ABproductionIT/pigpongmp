import socket
import json


jsonResult = {"first":"You're", "second":"Awsome!"}
jsonResult = json.dumps(jsonResult)

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
    ClientSocket.send(str(jsonResult).encode('utf-8'))
    Response = ClientSocket.recv(1024)
    print(Response)

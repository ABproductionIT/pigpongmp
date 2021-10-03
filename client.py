import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233


print('Waiting for connection')
ClientSocket.connect((host, port))


while True:
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

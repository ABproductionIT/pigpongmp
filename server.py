import socket
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    welcome = 'Welcome to the Server'
    connection.send(welcome.encode('utf-8'))
    while True:
        data = listcli[0].recv(1024)
        reply = data.decode('utf-8')
        print(reply, connection)
        if not data:
            pass
        listcli[1].send(reply.encode("utf-8"))


listcli=[]

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    listcli.append(Client)
    print(Client)
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

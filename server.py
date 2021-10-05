import socket
from _thread import *
import json

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
        if connection == listcli[0]:
            data = listcli[0].recv(2048)
            reply = data.decode('utf-8')
            if not data:
                pass
            try:
                listcli[1].send(reply.encode("utf-8"))
            except:
                pass
        elif connection == listcli[1]:
            data = listcli[1].recv(2048)
            reply = data.decode('utf-8')
            if not data:
                pass
            listcli[0].send(reply.encode("utf-8"))


listcli = []
listcodep1 = []
listcodep2 = []

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    dostup = Client.recv(2048)
    code = json.loads(dostup)
    if code['player'] == 1:
       jsoncode = {code['code']: Client}
       listcodep1.append(jsoncode)
    elif code['player'] == 2:
       jsoncode = {code['code']: Client}
       listcodep2.append(jsoncode)
    else:
        pass
    print(listcodep1, listcodep2)
    listcli.append(Client)
    print(Client)
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))

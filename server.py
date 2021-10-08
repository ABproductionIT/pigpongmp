import socket
from _thread import *
import json

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)
playerList = {}

def threaded_client(connection, code):
    welcome = 'Welcome to the Server'
    connection.send(welcome.encode('utf-8'))
    while True:
        if connection == playerList[code]['player1']:
            data = playerList[code]['player1'].recv(2048)
            reply = data.decode('utf-8')
            if not data:
                pass
            try:
                playerList[code]['player2'].send(reply.encode("utf-8"))
            except:
                pass
        elif connection == playerList[code]['player2']:
            data = playerList[code]['player2'].recv(2048)
            reply = data.decode('utf-8')
            if not data:
                pass
            try:
                playerList[code]['player1'].send(reply.encode("utf-8"))
            except:
                pass

while True:
    hasConnect = False
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    code = json.loads(Client.recv(2048))
    if code['code'] in playerList.keys():
        if 'player2' not in playerList[code['code']]:
            hasConnect = True
            playerList[code['code']][code['player']] = Client
    else:
        hasConnect = True
        playerList[code['code']] = {
            code['player']: Client
        }
    if hasConnect:
        start_new_thread(threaded_client, (Client, code['code'] ))

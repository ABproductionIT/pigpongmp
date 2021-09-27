import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))

server.listen()

while True:
    user, addres = server.accept()
    print("connect")
    user.send("you are connect".encode("utf-8"))

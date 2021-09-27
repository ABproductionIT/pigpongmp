import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client1.connect(("127.0.0.1", 12346))


while True:
    data = client.recv(1024)
    print(data.decode("utf-8"))
    datax = client1.recv(1024)
    t = datax.decode("utf-8")


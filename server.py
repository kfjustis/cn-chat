#1/usr/bin/python

import socket

print("Starting server, waiting for client...")
sock = socket.socket()
host = socket.gethostname()
port = 1000

sock.bind((host, port))
sock.listen(5)
con = None

while True:
    if con is None:
        # Wait here
        print("Waiting for connection...")
        con, addr = sock.accept()
        print("Received connection from: " + str(addr))
    else:
        # Wait here also
        print("Waiting for response...")
        print(sock.recv(1024))
        data = input("Type a message for the client: ")
        con.send(str.encode(data))

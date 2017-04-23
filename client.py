#!/usr/bin/python

import socket

sock = socket.socket()
host = socket.gethostname()
port = 1000

sock.connect((host, port))
print("Connected to :" + str(host))

while True:
    data = input("Type a message for the server: ")
    sock.send(str.encode(data))
    print("Waiting for response...")
    print(sock.recv(1024))

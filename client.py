#!/usr/bin/python

import socket

def Main():
    host = socket.gethostname()
    port = 5000

    localSocket = socket.socket()
    localSocket.connect((host, port))

    message = input("Message(-1 to send): ")

    while message != '-1':
        localSocket.send(message.encode())
        data = localSocket.recv(1024).decode()
        print("->: " + data)
        message = input("Message(-1 to send): ")

    localSocket.close()

if __name__ == '__main__':
    Main()

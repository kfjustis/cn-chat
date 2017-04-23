#1/usr/bin/python

import socket

def Main():

    host = socket.gethostname()
    port = 5000

    localSocket = socket.socket()
    localSocket.bind((host, port))

    localSocket.listen(1)
    conn, addr = localSocket.accept()
    print("Received connection from: " + str(addr))

    while True:
        data = conn.recv(1024).decode()

        if not data:
            break
        elif (str(data) == 'exit()'):
            print("Tried to exit!")

        print("Client says: " + str(data))
        conn.send(data.encode())

    conn.close()

if __name__ == '__main__':
    Main()

import socket
import sys

def Main():
    # connect and ask for username
    host = socket.gethostname()
    port = 12450
    localSocket = socket.socket()
    localSocket.connect((host, port))
    print()
    print("Connected to " + str(host) + '/' + str(port) + '!')
    message = input("\nUsername: ")
    localSocket.send(message.encode())

    waiting = True
    while waiting is True:
        response = localSocket.recv(1024).decode()
        if response == "ack":
            break
        elif response == "error":
            print("\nInvalid username! Terminating client...")
            localSocket.close()
            sys.exit()
        else:
            print("Waiting for server response...")

    print("\nUsername matched by server!")
    '''
    # connect and ask for password
    localSocket = socket.socket()
    localSocket.connect((host, port))
    print()
    message = input("\nPassword: ")
    localSocket.send(message.encode())
    localSocket.close()
    '''

if __name__ == '__main__':
    Main()

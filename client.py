import socket
import sys

def wait_for_server(error_msg, connection):
    waiting = True
    while waiting == True:
        response = connection.recv(1024).decode()
        if response == "ack":
            waiting = False
        elif response == "error":
            print(error_msg)
            print("here")
        elif response == "invalid_command":
            waiting = False
            print(error_msg)
            message = input("\nEnter command: ")
            connection.send(message.encode())
            return "invalid command"
        else:
            print("Error was: " + error_msg)
            print("Waiting for server response...")

    return True

def Main():
    # vars
    ack = "ack"
    error = "error"

    # connect and ask for username
    host = socket.gethostname()
    port = 12450
    localSocket = socket.socket()
    localSocket.connect((host, port))
    print()
    print("Connected to " + str(host) + '/' + str(port) + '!')

    # ask for command
    message = input("\nEnter command: ")

    # handle sending command
    localSocket.send(message.encode())

    # wait for valid response
    while wait_for_server("\nCommand invalid! If you haven't logged in, please do so.",
        localSocket) == "invalid command":
        print("loop")
        pass

    message = input("\nUsername: ")
    localSocket.send(message.encode())
    wait_for_server("\nInvalid username! Terminating client...", localSocket)
    '''
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
    '''

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

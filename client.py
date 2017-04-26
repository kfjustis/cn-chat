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
            connection.close()
            sys.exit()
        elif response == "invalid_command":
            waiting = False
            print(error_msg)
            message = input("\nEnter command: ")
            connection.send(message.encode())
            return "invalid command"
        elif response == "inavlid_username":
            waiting = False
            print(error_msg)
            message = input("\nUsername: ")
            connection.send(message.encode())
            return "invalid_username"
        else:
            waiting = False
            print("Error was: " + error_msg)
            print("Waiting for server response...")

    return True

def Main():
    # vars
    ack = "ack"
    error = "error"
    running = False

    # connect and ask for username
    host = socket.gethostname()
    port = 12450
    localSocket = socket.socket()
    try:
        localSocket.connect((host, port))
    except socket.error as err:
        print("\nClient could not connect to server :: ERROR : %s\n" % err)
        print("Make sure you've started the server before you connect the client!\n")
        sys.exit()
    print()
    print("Connected to " + str(host) + '/' + str(port) + '!')

    # ask for command
    message = input("\nEnter command: ")

    # handle sending command
    localSocket.send(message.encode())

    # wait for valid command
    while wait_for_server("\nCommand invalid or exited! If you haven't logged in, please do so.",
        localSocket) == "invalid command":
        pass

    # need to handle commands in loop, we are logged in by here
    running = True
    while running:
        message = input("Enter command: ")
        localSocket.send(message.encode())

        while wait_for_server("\nCommand invalid or exited! If you haven't logged in, please do so.",
            localSocket) == "invalid command":
            pass


if __name__ == '__main__':
    Main()

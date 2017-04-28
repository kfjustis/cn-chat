import socket
import sys

def wait_for_server(error_msg, connection):
    waiting = True
    while waiting:
        response = connection.recv(1024).decode()
        opts = response.split()
        if opts[0] == "ack":
            waiting = False
        elif opts[0] == "ack_message":
            # have to cleanup the list to print for client
            foundGuest = False
            opts.remove("ack_message")
            for item in opts:
                if item == "send":
                    opts.remove("send")
                if item == "Guest:":
                    foundGuest = True
            # convert list to string and print
            message = " ".join(opts)
            if not foundGuest:
                print(message)
            else:
                print("Server: (0) Exited or command invalid! If you haven't logged in, please do so.")
            waiting = False
        elif opts[0] == "ack_login":
            opts.remove("ack_login")
            uname = opts[0]
            print("Server: " + str(uname) + " joins.")
            waiting = False
        elif opts[0] == "ack_exit":
            opts.remove("ack_exit")
            uname = opts[0]
            print("Server: " + str(uname) + " left.\n")
            connection.close()
            sys.exit()
        elif opts[0] == "ack_new_user":
            opts.remove("ack_new_user")
            uname = opts[0]
            print("Server: Created user " + "'" + str(uname) + "'")
            waiting = False
        elif opts[0] == "ack_bad_password":
            print("Server: Incorrect password!")
            waiting = False
        elif opts[0] == "ack_bad_newuser":
            print("Server: Could not create user! Too long or already exists.")
            waiting = False
        else: # Some other error I haven't thought of
            print(error_msg)
            waiting = False

    return True

def Main():
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
    #print("Connected to " + str(host) + '/' + str(port) + '!')
    print("My chat room client. Version One.")

    # ask for command
    message = input("Enter command: ")

    # handle sending command
    localSocket.send(message.encode())

    # wait for valid command
    while wait_for_server("Server: (1) Exited or command invalid! If you haven't logged in, please do so.",
        localSocket) == "invalid command":
        pass

    # need to handle commands in loop, we are logged in by here
    running = True
    while running:
        message = input("\nEnter command: ")
        localSocket.send(message.encode())

        while wait_for_server("Server: (2) Exited or command invalid! If you haven't logged in, please do so.",
            localSocket) == "invalid command":
            pass


if __name__ == '__main__':
    Main()

import socket
import sys

def print_error_and_send(error_msg, connection):
    print(error_msg)
    error = "error"
    connection.send(error.encode())

def check_commands(input_command, comm_list):
    for comm in comm_list:
        if input_command == comm:
            return True

    return False

def Main():
    # vars
    ack = "ack"
    error = "error"
    invalid_command = "invalid_command"
    running = True
    login = False
    commandFailing = False
    commandList = ["send", "login", "logout"]

    # read users from file
    file = open("accounts.txt", "r")
    userInfo = file.read().splitlines()

    # connect to verify login
    host = socket.gethostname()
    port = 12450
    localSocket = socket.socket()
    localSocket.bind((host, port))
    localSocket.listen(5)
    conn, addr = localSocket.accept()
    if conn:
        running = True

    # handle reading command (MUST WAIT FOR VALID COMMAND)
    while running != False:
        command = conn.recv(1024).decode()
        if not command:
            print_error_and_send("Invalid data! Terminating server...", conn)
            connection.close()
            sys.exit()

        validCommand = check_commands(command, commandList)
        while validCommand == False and login == False:
            if command == "login":
                conn.send(ack.encode())
                print("\nValidating login...")
                login = True
            else:
                print("Command denied. Please login first.")
                conn.send(invalid_command.encode())
                command = conn.recv(1024).decode()
                if not command:
                    print_error_and_send("Invalid data! Terminating server...", conn)
                    # we don't want to close the connection and exit cause this
                    # should loop until the command is valid

        running = False

    # read username from client and validate
    print("\nConnection from: " + str(addr))
    running = True
    while running != False:
        conn.send(ack.encode())
        username = conn.recv(1024).decode()
        if not username:
            print_error_and_send("Invalid data! Terminating server...", conn)
            conn.close()
            sys.exit()

        validUname = False
        for name in userInfo:
            if name == username:
                validUname = True

        if (validUname == False):
            print_error_and_send("Username not found! Terminating server...", conn)
            conn.close()
            sys.exit()

        print("\nUsername found!")

        running = False
        conn.send(ack.encode())

    '''
    # read password from client and validate
    #conn, addr = localSocket.accept()
    if conn:
        running = True
    while running is not False:
        password = conn.recv(1024).decode()
        if not password:
            print_error_and_send("Invalid data! Terminating server...", conn)

        validPword = False
        for name in userInfo:
            if name == password:
                validPword = True

        if (validUname == False):
            print_error_and_send("Password not found! Terminating server...", conn)

        print("Password found!")

        running = False

    '''
    # close socket and exit
    localSocket.close()
    sys.exit()

if __name__ == '__main__':
    Main()

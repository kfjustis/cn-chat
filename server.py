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

def check_username_or_password(input_info, uInfoList):
    for info in uInfoList:
        if input_info == info:
            return True

    return False

def Main():
    # vars
    ack = "ack"
    error = "error"
    invalid_command = "invalid_command"
    invalid_username = "invalid_username"
    running = True
    login = False
    commandFailing = False
    commandList = ["send", "login", "logout"]
    currentUser = None

    # read users from file
    file = open("accounts.txt", "r")
    userInfoList = file.read().splitlines()

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
    while running:
        command = conn.recv(1024).decode()
        if not command:
            print_error_and_send("Invalid data! Terminating server...", conn)
            conn.close()
            sys.exit()

        # just looking to make sure the command contains login
        validCommand = check_commands(command, commandList)
        print(validCommand)
        print(login)
        while validCommand == False or login == False:
            opts = command.split()
            if command == "login":
                opts = command.split()
                if len(opts) != 3:
                    print_error_and_send("(1) Invalid use of login command! Terminating server...", conn)
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                elif opts[0] != "login":
                    print_error_and_send("(2) Invalid use of login command! Terminating server...", conn)
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                else:
                    conn.send(ack.encode())
                    login = True
            elif opts[0] == "exit":
                print_error_and_send("Server closed by client!", conn)
                conn.send(ack.encode())
                conn.close()
                sys.exit()
            elif opts[0] != "login":
                print_error_and_send("(3) Invalid use of login command! Terminating server...", conn)
                #conn.send(invalid_command.encode())
                '''
                testing
                '''
                conn.close()
                sys.exit()
            elif opts[0] == "login":
                if len(opts) != 3:
                    print_error_and_send("(4) Invalid use of login command! Terminating server...", conn)
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                else:
                    validCreds = False
                    if check_username_or_password(opts[1], userInfoList) == True: # check username
                        if check_username_or_password(opts[2], userInfoList) == True: # check password
                            print("here2")
                            conn.send(ack.encode())
                            login = True
                            validCommand = True
                            currentUser = opts[1]
                        else:
                            print_error_and_send("Invalid password! Terminating server...", conn)
                            #conn.send(error.encode())
                            conn.send(invalid_command.encode())
                            conn.close()
                            sys.exit()
                    else:
                        print_error_and_send("Invalid username! Terminating server...", conn)
                        conn.send(error.encode())
                        conn.close()
                        sys.exit()
            else:
                print("Command denied. Please login first.")
                conn.send(invalid_command.encode())
                command = conn.recv(1024).decode()
                if not command:
                    print_error_and_send("Invalid data! Terminating server...", conn)
                    '''
                    NOTICE!
                    we don't want to close the connection and exit cause this
                    should loop until the command is valid
                    '''

        running = True

    # close socket and exit
    localSocket.close()
    sys.exit()

if __name__ == '__main__':
    Main()

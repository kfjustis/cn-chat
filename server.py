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
    ack_message = "ack_message"
    ack_exit = "ack_exit"
    error = "error"
    invalid_command = "invalid_command"
    invalid_username = "invalid_username"
    running = True
    login = False
    commandFailing = False
    commandList = ["send", "login", "newuser", "exit"]
    currentUser = None

    # read users from file
    file = open("accounts.txt", "r")
    userInfoList = file.read().splitlines()
    file.close()

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
        opts = command.split()
        if not command:
            print_error_and_send("Invalid data! Terminating server...", conn)
            conn.close()
            sys.exit()

        # just looking to make sure the command contains login
        validCommand = check_commands(opts[0], commandList)
        print("login state: " + str(login))
        if validCommand:
            if opts[0] != "login" and login == False:
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
            if opts[0] == "login":
                if len(opts) != 3:
                    print_error_and_send("(1) Invalid use of login command! Terminating server...", conn)
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                # validate credentials that were passed
                validCreds = False
                if check_username_or_password(opts[1], userInfoList) == True: # check username
                    if check_username_or_password(opts[2], userInfoList) == True: # check password
                        conn.send(ack.encode())
                        login = True
                        validCommand = True
                        currentUser = opts[1]
                        print("login state after login: " + str(login))
                        print("logged in as: " + str(currentUser))
                    else:
                        print_error_and_send("Invalid password! Terminating server...", conn)
                        conn.send(invalid_command.encode())
                        conn.close()
                        sys.exit()
                else:
                    print_error_and_send("Invalid username! Terminating server...", conn)
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                # END LOGIN LOGIC
            if opts[0] == "exit":
                print_error_and_send("Server closed by client!", conn)
                optList = []
                optList.append(ack_exit)
                if (currentUser is not None):
                    optList.append(currentUser)
                else:
                    optList.append("Guest")
                optString = " ".join(optList)
                print(optString)
                conn.send(optString.encode())
                conn.close()
                sys.exit()
                # END EXIT LOGIC
            if opts[0] == "send":
                # must build opt list then send as a string
                optList = []
                optList.append(ack_message)
                optList.append(currentUser + ":")
                for opt in opts:
                    optList.append(opt)
                optString = " ".join(optList)
                conn.send(optString.encode())
                # END SEND LOGIC
            if opts[0] == "newuser":
                uname = opts[1]
                pword = opts[2]
                # write account to file (has criteria)
                file = open("accounts.txt", "a+")
                file.write("\n" + str(uname) + "\n"+ str(pword))
                file.close()
                conn.send(ack.encode())
                #END NEWUSER LOGIC
        else: # command was not even an existing/recognized command
            print_error_and_send("Command does not exist! Terminating server...", conn)
            conn.send(invalid_command.encode())
            conn.close()
            sys.exit()

            '''
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
            elif opts[0] == "send":
                # need to get string without the send command
                # need to concat received message with the ack for client to see it
                print("WE ARE SENDING THE SEND")
                ack_message = ack_message + str(opts[1:])
                conn.send(ack_message.encode())
            elif opts[0] != "login" and opts[0] != "send":
                print_error_and_send("(3) Invalid use of login command! Terminating server...", conn)
                #conn.send(invalid_command.encode())

                testing
                a
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

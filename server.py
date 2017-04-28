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
    if not input_info:
        return False

    for info in uInfoList:
        if input_info == info:
            return True

    return False

def Main():
    # vars
    ack = "ack"
    ack_message = "ack_message"
    ack_login = "ack_login"
    ack_bad_password = "ack_bad_password"
    ack_exit = "ack_exit"
    error = "error"
    invalid_command = "invalid_command"
    invalid_username = "invalid_username"
    invalid_password = "invalid_password"
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
        #print("login state: " + str(login))
        if validCommand:
            if opts[0] != "login" and opts[0] != "exit" and login == False:
                #print("Command denied. Please login first.")
                conn.send(invalid_command.encode())
                command = conn.recv(1024).decode()
                opts = command.split()
                if not command:
                    print_error_and_send("Invalid data! Terminating server...", conn)
                    '''
                    NOTICE!
                    we don't want to close the connection and exit cause this
                    should loop until the command is valid
                    '''

            if opts[0] == "login":
                if len(opts) != 3:
                    #print_error_and_send("(1) Invalid use of login command! Terminating server...", conn)
                    conn.send(invalid_command.encode())
                elif check_username_or_password(opts[1], userInfoList): # check username
                    #if check_username_or_password(opts[2], userInfoList): # check password
                    unameIndex = userInfoList.index(opts[1])
                    pwordIndex = unameIndex + 1
                    if (userInfoList[pwordIndex] == opts[2]): # check actual password
                        #conn.send(ack.encode())
                        login = True
                        currentUser = opts[1]
                        optList = []
                        optList.append(ack_login)
                        optList.append(currentUser)
                        optString = " ".join(optList)
                        conn.send(optString.encode())
                        #print("login state after login: " + str(login))
                        #print("logged in as: " + str(currentUser))
                    else:
                        #print_error_and_send("Invalid password! Terminating server...", conn)
                        conn.send(ack_bad_password.encode())
                        #conn.close()
                        #sys.exit()
                else:
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                # END LOGIN LOGIC
            elif opts[0] == "exit":
                # print_error_and_send("Server closed by client!", conn)
                optList = []
                optList.append(ack_exit)
                if (currentUser is not None):
                    running = False
                    optList.append(currentUser)
                    optString = " ".join(optList)
                    conn.send(optString.encode())
                else:
                    optList.append("Guest")
                    optString = " ".join(optList)
                    #print(optString)
                    conn.send(optString.encode())
                    conn.close()
                    sys.exit()
                    # END EXIT LOGIC
            elif opts[0] == "send":
                # must build opt list then send as a string
                optList = []
                optList.append(ack_message)
                if currentUser is None:
                    currentUser = "Guest"
                optList.append(currentUser + ":")
                for opt in opts:
                    optList.append(opt)
                optString = " ".join(optList)
                conn.send(optString.encode())
                # END SEND LOGIC
            elif opts[0] == "newuser":
                uname = opts[1]
                pword = opts[2]

                # usernames and passwords must follow criteria


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

    # close socket and exit
    localSocket.close()
    sys.exit()

if __name__ == '__main__':
    Main()

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
    ack_new_user = "ack_new_user"
    ack_bad_password = "ack_bad_password"
    ack_bad_newuser = "ack_bad_newuser"
    ack_exit = "ack_exit"
    error = "error"
    invalid_command = "invalid_command"
    running = True
    login = False
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

    # no use in running the loop if we couldn't connect
    if conn:
        running = True

    # handle reading command (MUST WAIT FOR VALID COMMAND)
    while running:
        command = conn.recv(1024).decode()
        opts = command.split()
        if not command:
            conn.close()
            sys.exit()
        # just looking to make sure the command contains login
        validCommand = check_commands(opts[0], commandList)
        if validCommand:
            if opts[0] != "login" and opts[0] != "exit" and login == False:
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
                    conn.send(invalid_command.encode())
                elif check_username_or_password(opts[1], userInfoList): # check username
                    unameIndex = userInfoList.index(opts[1])
                    pwordIndex = unameIndex + 1
                    if (userInfoList[pwordIndex] == opts[2]): # check actual password
                        login = True
                        currentUser = opts[1]
                        optList = []
                        optList.append(ack_login)
                        optList.append(currentUser)
                        optString = " ".join(optList)
                        conn.send(optString.encode())
                    else:
                        conn.send(ack_bad_password.encode())
                else:
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                # END LOGIN LOGIC
            elif opts[0] == "exit":
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
                if (0 < len(uname) < 32):
                    if not check_commands(uname, userInfoList):
                        # write account to file (has criteria)
                        file = open("accounts.txt", "a+")
                        file.write("\n" + str(uname) + "\n"+ str(pword))
                        file.close()

                        # send ack that we created a new user
                        optList = []
                        optList.append(ack_new_user)
                        optList.append(uname)
                        optString = " ".join(optList)
                        conn.send(optString.encode())
                    else:
                        conn.send(ack_bad_newuser.encode())
                else:
                    conn.send(ack_bad_newuser.encode())
                # END NEWUSER LOGIC
        else: # command was not even an existing/recognized command
            conn.send(invalid_command.encode())

    # close socket and exit
    localSocket.close()
    sys.exit()

if __name__ == '__main__':
    Main()

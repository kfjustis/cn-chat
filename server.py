import socket
import sys

'''
Terrible function for managing errors with the client. Don't use.
'''
def print_error_and_send(error_msg, connection):
    print(error_msg)
    error = "error"
    connection.send(error.encode())

'''
Checks to see if the "input_command" exists in the "comm_list".
In other words, this controls whether a command exists or not.
All new commands must be added to the "comm_list" on the server
to function properly.

Returns True if found, False if not
'''
def check_commands(input_command, comm_list):
    for comm in comm_list:
        if input_command == comm:
            return True

    return False

'''
Checks to see if "input_info" exists in the "uInfoList".

Returns True if found, False if not
'''
def check_username_or_password(input_info, uInfoList):
    if not input_info:
        return False

    for info in uInfoList:
        if input_info == info:
            return True

    return False

def Main():
    # vars
    ack_message = "ack_message"
    ack_login = "ack_login"
    ack_new_user = "ack_new_user"
    ack_bad_password = "ack_bad_password"
    ack_bad_newuser = "ack_bad_newuser"
    ack_bad_newuser_pword = "ack_bad_newuser_pword"
    ack_exit = "ack_exit"
    error = "error"
    invalid_command = "invalid_command"
    running = True
    login = False
    commandList = ["send", "login", "newuser", "logout"]
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

    print("\nMy chat room server. Version One.")

    # no use in running the loop if we couldn't connect
    if conn:
        running = True

    # handle reading command (MUST WAIT FOR VALID COMMAND)
    while running:
        # read users from file
        file = open("accounts.txt", "r")
        userInfoList = file.read().splitlines()
        file.close()

        command = conn.recv(1024).decode()
        opts = command.split()
        if not command:
            conn.close()
            sys.exit()
        # we only care about command that exist, of course
        validCommand = check_commands(opts[0], commandList)
        if validCommand:
            if opts[0] != "login" and opts[0] != "logout" and login == False:
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
                        print(str(currentUser) + " login.")
                    else: # username was fine, but password was bad
                        conn.send(ack_bad_password.encode())
                else: # default catch
                    conn.send(error.encode())
                    conn.close()
                    sys.exit()
                # END LOGIN LOGIC
            elif opts[0] == "logout":
                '''
                Here we create a list of data that the client uses usually of the form:
                <command code> <username/password/something> <extra data>. This list is
                then joined into a string, which gets encoded and sent to the client. In
                the client, the string is then split again back into an arg list and is
                interpreted in different ways depending on the function. This works pretty
                much the same way for the rest of the functions in this file.
                '''
                optList = []
                optList.append(ack_exit)
                if (currentUser is not None):
                    running = False
                    optList.append(currentUser)
                    optString = " ".join(optList)
                    conn.send(optString.encode())
                    print(str(optList[1]) + " logout.")
                else: # if we don't have a user logged in, give the program something
                    optList.append("Guest")
                    optString = " ".join(optList)
                    conn.send(optString.encode())
                    print("Guest logout.")
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
                # we only want the message out of the option list, so remove baggage...
                optList.pop(0)
                optList.pop(0)
                optList.pop(0)
                optString = " ".join(optList)
                print(str(currentUser) + ": " + str(optString))
                # END SEND LOGIC
            elif opts[0] == "newuser":
                if len(opts) != 3:
                    conn.send(ack_bad_newuser.encode())
                else:
                    uname = opts[1]
                    pword = opts[2]
                    # usernames and passwords must follow criteria
                    if (0 < len(uname) < 32): # username must follow a certain length
                        # username must not exist already
                        if not check_commands(uname, userInfoList):
                            if (4 <= len(pword) <= 8): # password must be certain length
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
                                print("New user created: " + str(optList[1]))
                            else:
                                conn.send(ack_bad_newuser_pword.encode())
                        else:
                            conn.send(ack_bad_newuser.encode())
                    else:
                        conn.send(ack_bad_newuser.encode())
                    # END NEWUSER LOGIC
            else: # command was valid but deprecated
                conn.send(invalid_command.encode())
        else: # command was not even an existing/recognized command
            conn.send(invalid_command.encode())

    # close socket and exit
    localSocket.close()
    sys.exit()

if __name__ == '__main__':
    Main()

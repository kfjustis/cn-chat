import socket
import sys

def print_error_and_exit(e_msg, connection):
    print(e_msg)
    error = "error"
    connection.send(error.encode())
    connection.close()
    sys.exit()

def Main():
    # vars
    ack = "ack"
    error = "error"

    # read users from file
    file = open("accounts.txt", "r")
    userInfo = file.read().splitlines()

    # connect to verify login
    host = socket.gethostname()
    port = 12450
    localSocket = socket.socket()
    localSocket.bind((host, port))
    localSocket.listen(5)

    # read username from client and validate
    conn, addr = localSocket.accept()
    print("\nConnection from: " + str(addr))
    if conn:
        running = True
    while running is not False:
        username = conn.recv(1024).decode()
        if not username:
            print_error_and_exit("Invalid data! Terminating server...", conn)

        validUname = False
        for name in userInfo:
            if name == username:
                validUname = True

        if (validUname == False):
            print_error_and_exit("Username not found! Terminating server...", conn)

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
            print_error_and_exit("Invalid data! Terminating server...", conn)

        validPword = False
        for name in userInfo:
            if name == password:
                validPword = True

        if (validUname == False):
            print_error_and_exit("Password not found! Terminating server...", conn)

        print("Password found!")

        running = False

    '''
    # close socket and exit
    localSocket.close()
    sys.exit()

if __name__ == '__main__':
    Main()

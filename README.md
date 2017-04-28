# cn-chat
Simple client-server chat program written in Python.

# Instructions
The client and server modules must be ran in separate windows and requires
a current installation of Python 3. Non-windows environments may have to use
```python3 <file_name.py>``` to launch the python files.

Window 1:

    python server.py

Window 2:

    python client.py

Commands:

```login <username> <password>``` :: Login to the server with valid username and
password.

    ex: login Tom Tom11

```send <message>``` :: Send a message to the server (like a chat room).

    ex: send How's it hangin'?

```newuser <username> <password>``` :: Creates a new user with login credentials.

    ex: newuser SuperDude coolguy25

```logout``` :: Logs the user out (closes the server and client connection) and
ends the program.

    ex: Come on now...

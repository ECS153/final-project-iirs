import socket

from . import *
from .gui import ChatWindow
from .server_connection import ServerConnection

HOST = socket.gethostname()  # For testing we will use same machine
PORT = 12345  # Arbitrary port for connecting

def main():
    login()
    server_connection = ServerConnection(HOST, PORT)
    while True:
        if valid_user():
            window = ChatWindow(server_connection)
            window.mainloop()
        else:
            break

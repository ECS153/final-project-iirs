import socket

from . import *
from .gui import ChatWindow
from .server_connection import ServerConnection
from .chat_session import ChatSession

HOST = socket.gethostname()  # For testing we will use same machine
PORT = 12345  # Arbitrary port for connecting

def main():
    username, password, private_key = register_or_login()
    server_connection = ServerConnection(HOST, PORT, username)
    while True:
        dest, dest_public_key = valid_user(server_connection, username)
        if dest:
            print(private_key, dest_public_key)
            session = ChatSession(server_connection, username, private_key, dest, dest_public_key)
            window = ChatWindow(session)
            window.mainloop()

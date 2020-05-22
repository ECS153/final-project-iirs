import socket

from . import *
from .gui import ChatWindow
from .server_connection import ServerConnection
from .chat_session import ChatSession

HOST = socket.gethostname()  # For testing we will use same machine
PORT = 12345  # Arbitrary port for connecting

def main():
    username, password = login()
    server_connection = ServerConnection(HOST, PORT)
    while True:
        dest = valid_user()
        if dest:
            session = ChatSession(server_connection, username, dest)
            window = ChatWindow(session)
            window.mainloop()
        else:
            break

from . import *
from .gui import ChatWindow

def main():
    login()
    server_socket = connect_To_Server()
    while True:
        if valid_user():
            window = ChatWindow(server_socket)
            window.mainloop()
        else:
            break

from . import *
from .gui import ChatWindow

def main():
    login()
    server_socket = connect_To_Server()
    window = ChatWindow(server_socket)
    window.mainloop()

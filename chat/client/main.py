from . import connect_To_Server
from .gui import ChatWindow

def main():
    server_socket = connect_To_Server()
    window = ChatWindow(server_socket)
    window.mainloop()

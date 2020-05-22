import socket

from ..message import Message

class ServerConnection:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, message):
        encoded = message.to_json().encode('utf-8') + b'\n'
        self.sock.sendall(encoded)

        # XXX
        data = self.sock.recv(1024).decode('utf-8')
        if '\n' in data:
            return Message.from_json(data[:data.index('\n')])
        else:
            return None

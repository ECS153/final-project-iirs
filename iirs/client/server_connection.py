import socket
import threading

from ..message import Message

class ServerConnection:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.recv_thread = ReceiveThread(self.sock)
        self.recv_thread.start()

    def send(self, message):
        encoded = message.to_json().encode('utf-8') + b'\n'
        self.sock.sendall(encoded)

    def recv(self):
        messages = []
        if '\n' in self.recv_thread.recv_buffer:
            text, self.recv_thread.recv_buffer = self.recv_thread.recv_buffer.split('\n', 1)
            messages.append(Message.from_json(text))

        return messages

class ReceiveThread(threading.Thread):
    recv_buffer = ''

    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        while True:
            self.recv_buffer += self.sock.recv(1024).decode('utf-8')

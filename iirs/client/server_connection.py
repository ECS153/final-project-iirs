import socket
import threading
import time

from ..message import Message

POLL_INTERVAL = .5

class ServerConnection:
    recv_buffer = ''

    def __init__(self, host, port, username):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.username = username

        self.recv_thread = ReceiveThread(self)
        self.recv_thread.start()

        self.poll_thread = PollThread(self)
        self.poll_thread.start()

    def send(self, message):
        encoded = message.to_json().encode('utf-8') + b'\n'
        self.sock.sendall(encoded)

    def poll(self):
        self.send(Message(self.username, None, None))

    def recv(self):
        messages = []
        if '\n' in self.recv_buffer:
            text, self.recv_buffer = self.recv_buffer.split('\n', 1)
            messages.append(Message.from_json(text))

        return messages

class PollThread(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def run(self):
        while True:
            time.sleep(POLL_INTERVAL)
            self.connection.poll()

class ReceiveThread(threading.Thread):
    recv_buffer = ''

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def run(self):
        while True:
            self.connection.recv_buffer += self.connection.sock.recv(1024).decode('utf-8')

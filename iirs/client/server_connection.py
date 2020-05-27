import socket
import threading
import time
import queue

from ..message import Message

SEND_INTERVAL = .5

class ServerConnection:
    def __init__(self, host, port, username):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.username = username

        self.recv_thread = ReceiveThread(self)
        self.recv_thread.start()

        self.send_thread = SendThread(self)
        self.send_thread.start()

    def send(self, message):
        self.send_thread.queue.put(message)

    def recv(self):
        messages = []
        while True:
            try:
                messages.append(self.recv_thread.queue.get_nowait())
            except queue.Empty:
                break

        return messages

class SendThread(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.queue = queue.Queue()

    def run(self):
        while True:
            time.sleep(SEND_INTERVAL)

            try:
                message = self.queue.get_nowait()
            except queue.Empty:
                message = Message(self.connection.username, None, None)
            encoded = message.to_json().encode('utf-8') + b'\n'
            self.connection.sock.sendall(encoded)

class ReceiveThread(threading.Thread):

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.queue = queue.Queue()

    def run(self):
        recv_buffer = ''

        while True:
            recv_buffer += self.connection.sock.recv(1024).decode('utf-8')
            while '\n' in recv_buffer:
                text, recv_buffer = recv_buffer.split('\n', 1)
                message = Message.from_json(text)
                self.queue.put(message)

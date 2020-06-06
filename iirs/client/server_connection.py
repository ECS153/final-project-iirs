import socket
import ssl
import threading
import time
import queue

from ..message import Message

SEND_INTERVAL = .5

class ServerConnection:
    closed = False

    def __init__(self, host, port, username):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        self.sock = ssl.wrap_socket(sock)

        self.username = username

        self.recv_thread = ReceiveThread(self)
        self.recv_thread.start()

        self.send_thread = SendThread(self)
        self.send_thread.start()

    def send(self, message):
        if self.closed:
            raise ValueError

        self.send_thread.queue.put(message)

    def recv(self):
        if self.closed:
            raise ValueError

        messages = []
        while True:
            try:
                messages.append(self.recv_thread.queue.get_nowait())
            except queue.Empty:
                break

        return messages

    # Close socket and terminate threads (blocks until complete)
    def close(self):
        self.closed = True
        self.send_thread.terminate()
        self.recv_thread.terminate()
        self.send_thread.join()
        self.sock.shutdown(socket.SHUT_RDWR)
        self.recv_thread.join()

class SendThread(threading.Thread):
    terminated = False

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.queue = queue.Queue()

    def run(self):
        while True:
            time.sleep(SEND_INTERVAL)

            terminated = self.terminated

            try:
                message = self.queue.get_nowait()
            except queue.Empty:
                if terminated:
                    return
                message = Message(self.connection.username, None, None)

            encoded = message.to_json().encode('utf-8') + b'\n'
            self.connection.sock.sendall(encoded)

    def terminate(self):
        self.terminated = True

class ReceiveThread(threading.Thread):
    terminated = False

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.queue = queue.Queue()

    def run(self):
        recv_buffer = ''

        while not self.terminated:
            recv_buffer += self.connection.sock.recv(1024).decode('utf-8')
            print("[Client] Recieved message:", recv_buffer) # Debug 'Prints what client has recieved'
            while '\n' in recv_buffer:
                text, recv_buffer = recv_buffer.split('\n', 1)
                message = Message.from_json(text)
                self.queue.put(message)

    def terminate(self):
        self.terminated = True

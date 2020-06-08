import socket
import ssl
import threading
import time
import queue

from ..message import Message, PeerMessage
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.asymmetric import ec
from base64 import b64encode, b64decode

SEND_INTERVAL = 1

class ServerConnection:
    closed = False

    def __init__(self, host, port, username, ec_key=None, peer_ec_key=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        self.sock = ssl.wrap_socket(sock)

        self.username = username
        self.ec_key = ec_key
        self.peer_ec_key = peer_ec_key
        if ec_key is None or peer_ec_key is None:
            self.aes_key = None
        else:
            self.aes_key = AES(ec_key.exchange(ec.ECDH(), peer_ec_key))

        self.recv_thread = ReceiveThread(self)
        self.recv_thread.start()

        self.send_thread = SendThread(self, self.ec_key, self.peer_ec_key, self.aes_key)
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

    def __init__(self, connection, ec_key, peer_ec_key, aes_key):
        super().__init__()
        self.connection = connection
        self.queue = queue.Queue()
        self.ec_key = ec_key
        self.peer_ec_key = peer_ec_key
        self.aes_key = aes_key

    def run(self):
        while True:
            time.sleep(SEND_INTERVAL)

            terminated = self.terminated

            try:
                message = self.queue.get_nowait()
                encoded = message.to_json().encode('utf-8') + b'\n'
                self.connection.sock.sendall(encoded)
            except queue.Empty:
                if terminated:
                    return
                if self.aes_key is not None:
                    deaddrop = 0
                    peer_message = PeerMessage("$NULL$", deaddrop)
                    encrypted = peer_message.to_encrypted_bytes(self.ec_key, self.aes_key)
                    body = b64encode(encrypted).decode()
                    message = Message(self.connection.username, "1", body) # Todo. This "1" will have to be a global deaddrop variable.
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

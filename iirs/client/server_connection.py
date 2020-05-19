import socket

class ServerConnection:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send_message(self, message):
        encoded = str.encode(message)
        self.sock.sendall(encoded)
        data = self.sock.recv(1024)
        decoded = data.decode("utf-8")
        return decoded

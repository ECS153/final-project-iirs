from ..message import Message

# Represents a session exchanging messages with another user
class ChatSession:
    def __init__(self, server_connection, name, peer_name):
        self.server_connection = server_connection
        self.name = name
        self.peer_name = peer_name

    def send_message(self, body):
        # TODO: encrypt
        message = Message(self.name, self.peer_name, body)
        return self.server_connection.send(message)

    def recv_messages(self):
        return self.server_connection.recv()


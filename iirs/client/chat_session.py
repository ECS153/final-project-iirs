from base64 import b64encode, b64decode

from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.asymmetric import ec

from ..message import Message, PeerMessage

# Represents a session exchanging messages with another user
class ChatSession:
    def __init__(self, server_connection, name, ec_key, peer_name, peer_ec_key):
        self.server_connection = server_connection
        self.name = name
        self.ec_key = ec_key
        self.peer_name = peer_name
        self.peer_ec_key = peer_ec_key
        if ec_key is None or peer_ec_key is None:
            self.aes_key = None
        else:
            self.aes_key = AES(ec_key.exchange(ec.ECDH(), peer_ec_key))

    def send_message(self, body):
        if self.aes_key is not None:
            peer_message = PeerMessage(body)
            encrypted = peer_message.to_encrypted_bytes(self.ec_key, self.aes_key)
            body = b64encode(encrypted)

        message = Message(self.name, self.peer_name, body)
        return self.server_connection.send(message)

    def recv_messages(self):
        encrypted_messages = self.server_connection.recv()

        messages = []
        for i in encrypted_messages:
            if self.aes_key is not None:
                # XXX use binary instead of json with base64
                b = b64decode(i.body)
                i.body = PeerMessage.from_encrypted_bytes(b, self.peer_ec_key, self.aes_key)
            if i.body is not None:
                messages.append(i)

        return messages

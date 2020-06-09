from base64 import b64encode, b64decode
from sys import maxsize

from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.asymmetric import ec

from ..message import Message, PeerMessage

# Represents a session exchanging messages with another user
class ChatSession:
    def __init__(self, server_connection, name, ec_key, peer_name, peer_ec_key, dd_sync=None):
        self.server_connection = server_connection
        self.name = name
        self.ec_key = ec_key
        self.peer_name = peer_name
        self.peer_ec_key = peer_ec_key
        self.dd_sync = dd_sync
        self.listener = False
        self.generator = False
        if ec_key is None or peer_ec_key is None:
            self.aes_key = None
        else:
            self.aes_key = AES(ec_key.exchange(ec.ECDH(), peer_ec_key))

    def send_message(self, body):
        
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
                    if i.body.message.startswith("$TIME$"):
                        dest_time = int(i.body.message[6:])
                        source_time = self.dd_sync.first_message_time
                        i.body.message = "Connection established successfully"
                        print("Comparing dt: " + str(dest_time) + " with st: " + str(source_time))
                        if source_time < dest_time: # We are the generator
                            self.generator = True
                            print("[CLIENT] We are the generator!")
                            print("[CLIENT] Next deaddrop will be:", str(self.dd_sync.currentDD))
                        elif dest_time < source_time: # We are the listener
                            self.listener = True
                            print("[CLIENT] We are the listener!")
                            print("[CLIENT] Next deaddrop will be:", str(self.dd_sync.currentDD))
                        elif source_time == dest_time: # If there is a conflict, then try again
                            print("[CLIENT] WARNING! Time conflict!")
                            self.dd_sync.regen()
                            i.body = None
                            break
                    # Update next DD information
                    self.dd_sync.last_success = self.dd_sync.currentDD # Stores which DD last successful comm was at
                    if self.listener:
                        print("Updating the deaddrop from " + str(self.dd_sync.currentDD) + " to " + str(i.body.deaddrop))
                        self.dd_sync.listener_update(i.body.deaddrop,0)
                    elif self.generator:
                        self.dd_sync.last_success = self.dd_sync.currentDD
                        self.dd_sync.generate()
                        print("Generating new future deaddrop " + str(self.dd_sync.nextDD))
                    if i.body.message == "$NULL$":
                        i.body = None

            if i.body is not None:
                messages.append(i)

        return messages

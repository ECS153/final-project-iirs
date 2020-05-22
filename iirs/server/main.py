# Basic multi-client server implementation
# Server expects messages in format:
# $SourceID[len 1]$DestID[len 1]$Mode[R or X]$Message


import socket, ssl
from threading import Thread
from socketserver import ThreadingMixIn
from .mix_network import MixNetwork

from ..message import Message

HOST = socket.gethostname()  # For testing we will use same machine
PORT = 12345  # Arbitrary port for connecting
MSG_SIZE = 4096  # Size of the message sent / received

# Temporary buffers to store messages to users.
# This will be eventually unecessary with deadrops
message_queues = {}


class ConnectionThread(Thread):
    def __init__(self, host, port, conn, message_queue):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.conn = conn
        self.hpstring = str(host) + ":" + str(port)
        self.message_queue = message_queue
        print("[Server] Client connected at", self.hpstring)

    def get_messages(self, source_client):
        try:
            messages = message_queues[source_client]
            del message_queues[source_client]
            return messages
        except KeyError:
            return []
        except IndexError:
            return []

    def send_messages(self, messages):
        text = ''.join(Message.to_json(i) + '\n' for i in messages)
        self.conn.sendall(text.encode())

    def store_message(self, message):
        dest = message.dest

        if dest not in message_queues:
            message_queues[dest] = []

        message_queues[dest].append(message)

    def run(self):
        while True:
            data = self.conn.recv(MSG_SIZE).decode()
            if not data:
                print("[Server] Client " + self.hpstring + " has disconnected!", flush=True)
                return
            data_str = str(data)
            print("[Server] Received data from" + self.hpstring + ": " + data_str)

            # Decode data
            message = Message.from_json(data_str)
            # Check for messages
            data_send = self.get_messages(message.src)
            print("[Server] Data sent to " + self.hpstring + " : " + str(data_send))
            # Send messages
            self.send_messages(data_send)
            # Store messages
            if message.dest != None:
                self.store_message(message)


class DeadDrop():
    def __init__(self):
        print("This class will handle all of the dead drops")

    def handle_messages(self):
        print("handle the messages, take in new and pass pass along old")



def main():
    mix_net = MixNetwork()
    mix_net.mix_and_pass()
    while True:
        mix_net.listen()
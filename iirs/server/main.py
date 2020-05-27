# Basic multi-client server implementation
# Server expects messages in format:
# $SourceID[len 1]$DestID[len 1]$Mode[R or X]$Message


import socket, ssl
from threading import Thread
from socketserver import ThreadingMixIn
from .mix_network import MixNetwork

from ..message import Message
from .deaddrop import *

HOST = socket.gethostname()  # For testing we will use same machine
PORT = 12345  # Arbitrary port for connecting
MSG_SIZE = 4096  # Size of the message sent / received

# Temporary buffers to store messages to users.
# This will be eventually unecessary with deadrops
message_queues = {}
#store username, public key, encrypted password and tag, encrypted key for clients
#persistent storage? currently resets when restarting server, need to re register
client_info = {}
#stores the client info until received all pieces
temp_client_info = []


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
            #print ("[Server] Received data from " + self.hpstring + ": " + data_str)

            # Decode data
            message = Message.from_json(data_str)
            # Check for messages
            data_send = self.get_messages(message.src)
            #print("[Server] Data sent to " + self.hpstring + " : " + str(data_send))
            # Send messages
            self.send_messages(data_send)
            # Store messages
            if message.dest != None:
                if message.dest == "register":
                    temp_client_info.append(message.body)
                    if len(temp_client_info) == 5:
                        #username is key, value is (public key, password, private key, tag)
                        # TODO check if username taken already
                        client_info[temp_client_info[0]] = (temp_client_info[1], temp_client_info[2], temp_client_info[3], temp_client_info[4])
                        del temp_client_info[:]
                elif message.dest == "login":
                    client = client_info[message.src]
                    password = client[1]
                    # validate user entered password
                    ret_body = "valid" if message.body == password else "invalid"
                    ret_src = "server"
                    ret_dest = message.src

                    ret_message = Message(ret_src, ret_dest, ret_body)
                    self.send_messages([ret_message])

                    #if valid password, send user info as well
                    if ret_body == "valid":
                        pub_key_message = Message(ret_src, ret_dest, client[0])
                        #self.send_messages(pub_key_message)

                        priv_key_message = Message(ret_src, ret_dest, client[2])
                        #self.send_messages(priv_key_message)

                        tag_message = Message(ret_src, ret_dest, client[3])
                        #self.send_messages(tag_message)
                        messages = [pub_key_message, priv_key_message, tag_message]
                        self.send_messages(messages)
                    else:
                        self.send_messages([ret_message])
                elif message.dest == "validate":
                    ret_body = client_info[message.body][0] if message.body in client_info else "invalid user"
                    ret_src = "server"
                    ret_dest = message.src
                    ret_message = Message(ret_src, ret_dest, ret_body)
                    self.send_messages([ret_message])
                else:
                    self.store_message(message)





def main():
    dead_drop = DeaddropManager()
    mix_net = MixNetwork(dead_drop)
    mix_net.mix_and_pass()
    while True:
        mix_net.listen()
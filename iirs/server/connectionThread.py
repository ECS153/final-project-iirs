from ..message import Message
import socket
import ssl
from tempfile import NamedTemporaryFile
from threading import Thread
from socketserver import ThreadingMixIn
import datetime

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption 

# Basic multi-client server implementation
# Server expects messages in format:
# $SourceID[len 1]$DestID[len 1]$Mode[R or X]$Message

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
    def __init__(self, host, port, conn, incoming_queue, outgoing_queue):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.conn = conn
        self.hpstring = str(host) + ":" + str(port)
        self.incoming_queue = incoming_queue
        self.outgoing_queue = outgoing_queue
        self.srcstr = ""
        print("[Server] Client connected at", self.hpstring)

    def get_messages(self):
        # Delete incoming queue so that messages don't loop through network
        del self.incoming_queue[self.srcstr]
        try:
            #print("cT attempting to get messages for",self.username) # Debug 'This prints which username we are trying to get messages for'
            messages = self.outgoing_queue[self.username].body
            print("cT: Attempting to send messages") # Debug
            print("cT: Message queue contents (len: " + str(len(messages)) +")") # Debug 'This prints the num of messages stored'
            # Debug Start_Block
            # 'Prints the contents of each Message object'
            for i in messages:
                print("{Source: " + str(i.src) + " | Dest: " + str(i.dest) + " | Msg: " + str(i.body) + "}")
            # Debug End_Block
            #print("Outgoing queue before delete",self.outgoing_queue) # Debug 'Shows contents of outgoing_queue before deletion'
            del self.outgoing_queue[self.username]
            #print("Outgoing queue after delete",self.outgoing_queue) # Debug 'Shows contents of outgoing_queue after deletion'
            self.send_messages(messages)
        except KeyError:
            return []
        except IndexError:
            return []

    def send_messages(self, messages):
        text = ''.join(Message.to_json(i) + '\n' for i in messages)
        self.conn.sendall(text.encode())


    def store_message(self, message):
        src = message.src
        # Part of incoming queue deletion on line 46.
        if self.srcstr == "":
            self.srcstr = src

        if src not in self.incoming_queue:
            self.incoming_queue[src] = []

        self.incoming_queue[src].append(message)

    def run(self):
        while True:
            data = self.conn.recv(MSG_SIZE).decode()
            if not data:
                print("[Server] Client " + self.hpstring + " has disconnected!", flush=True)
                return
            data_str = str(data)
            #print ("[Server] Received data from " + self.hpstring + ": " + data_str) # Debug 'Prints where data was recieved from'
            # Decode data
            message = Message.from_json(data_str)
            self.username = message.src
            
            # Store messages
            if message.dest == "register":
                temp_client_info.append(message.body)
                if len(temp_client_info) == 4:
                    #username is key, value is (public key, password, private key)
                    # TODO check if username taken already
                    client_info[temp_client_info[0]] = (temp_client_info[1], temp_client_info[2], temp_client_info[3])
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

                    messages = [pub_key_message, priv_key_message]
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
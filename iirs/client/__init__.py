import socket
from getpass import getpass
import hashlib, queue

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, BestAvailableEncryption, load_pem_private_key, load_pem_public_key

from .server_connection import ServerConnection
from .chat_session import ChatSession

from sys import maxsize
from random import seed,randint
from time import time


HOST = socket.gethostname()  # For testing we will use same machine
PORT = 12345  # Arbitrary port for connecting

# Temp variable for now
NUM_DEADDROP = 100

class DeadDropSync:
    def __init__(self):
        seed(time())
        self.currentDD = 0
        self.nextDD = randint(1,NUM_DEADDROP)
        self.conn_status = False
        self.first_message_time = maxsize
        self.last_success = 0
        self.attempts = 0

    # Updates the deaddrops for a listener client
    def listener_update(self, currentDD, nextDD):
        if not self.conn_status:
            self.conn_status = True
        self.currentDD = currentDD
        self.nextDD = nextDD
    
    # Generates a new next deaddrop 
    def generate(self):
        if not self.conn_status:
            self.conn_status = True
        self.currentDD = self.nextDD
        self.nextDD = randint(1,NUM_DEADDROP)
    
    # Regenerates the next dead drop
    def regen(self):
        self.nextDD = randint(1,NUM_DEADDROP)

def register_or_login():
    private_key = None
    while private_key is None:
        command = input("Enter r to register or l to login:")
        (username, password) = query_login()
        if command == "r":
            private_key = register_user(username, password)
            #generate_session_keys(username, password)
            break
        elif command == "l":
            private_key = login(username, password)
        else:
            print("invalid command, try again")
    return (username, password, private_key)

def register_user(username, password):
    encryption_key, server_password, remainder = hash_password(password)
    return register(username, encryption_key, server_password, remainder)


def register(username, encryption_key, server_password, remainder):
    temp_server_connection = ServerConnection(HOST, PORT, username)
    temp_session = ChatSession(temp_server_connection, username, None, "register", None)

    key = ec.generate_private_key(ec.SECP256R1, default_backend()) #256 bit key
    public_key = key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode()
    secure_private_key = key.private_bytes(Encoding.PEM,
            PrivateFormat.PKCS8,
            BestAvailableEncryption(encryption_key.encode())).decode()

    #send username, server_password, public_key, and secure_private_key to server
    temp_session.send_message(username)
    temp_session.send_message(public_key)
    temp_session.send_message(server_password)
    temp_session.send_message(secure_private_key)

    temp_server_connection.close()

    return key

def hash_password(password):
    h = hashlib.sha512()
    h.update(str.encode(password)) #convert string password to bytes, hash
    digest = h.hexdigest()
    encryption_key = digest[:32] #use first 32 bytes as key
    remainder = digest[32:48] #use next 16 bytes to hold password on server
    server_password = digest[48:] #remainder, used as iv for encryption
    return encryption_key, server_password, remainder

# use usernmame and password to generate keys / do encryption
# Return The private key if successful, otherwise None
def login(username, password):
    encryption_key, server_password, remainder = hash_password(password)
    temp_server_connection = ServerConnection(HOST, PORT, username)
    temp_session = ChatSession(temp_server_connection, username, None, "login", None)

    temp_session.send_message(server_password)
    messages = []
    #second receive should receive 3 messages
    while len(messages) < 3:
        messages += temp_session.recv_messages()

    if messages[0].body != "valid":
        print("invalid password, try again")
        temp_server_connection.close()
        return None
    else:
        print("validated")
    public_key = messages[1].body
    secure_private_key = messages[2].body
    private_key = load_pem_private_key(secure_private_key.encode(), encryption_key.encode(), default_backend())
    temp_server_connection.close()
    return private_key


def query_login():
    username = input("Enter username:")
    password = getpass(prompt="Enter password:")
    return (username, password)

def valid_user(username):
    temp_server_connection = ServerConnection(HOST, PORT, username)
    dest = input("Enter username of user you want to talk to or q to quit:")
    if dest == "q": # Todo: This doesn't quit properly?
        temp_server_connection.close()
        return None, None
    temp_session = ChatSession(temp_server_connection, username, None, "validate", None)

    temp_session.send_message(dest)
    messages = []
    #second receive should receive 3 messages
    while len(messages) < 1:
        messages += temp_session.recv_messages()

    if messages[0].body == "invalid user":
        print("This user does not exist, please try again")
        temp_server_connection.close()
        return None, None

    # other users public key, used for decrypting messages in end to end encryption
    dest_public_key = load_pem_public_key(messages[0].body.encode(), default_backend())
    temp_server_connection.close()
    return dest, dest_public_key

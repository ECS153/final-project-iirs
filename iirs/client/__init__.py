import socket
from .server_connection import ServerConnection
from .chat_session import ChatSession
from getpass import getpass
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

HOST = socket.gethostname()  # For testing we will use same machine
PORT = 12345  # Arbitrary port for connecting

def register_or_login():
    loop = True
    while loop:
        command = input("Enter r to register or l to login:")
        (username, password) = query_login()
        if command == "r":
            register_user(username, password)
            #generate_session_keys(username, password)
            break
        elif command == "l":
            loop = login(username, password)
        else:
            print("invalid command, try again")
    return (username, password)

def register_user(username, password):
    encryption_key, server_password, remainder = hash_password(password)
    register(username, encryption_key, server_password, remainder)


def register(username, encryption_key, server_password, remainder):
    temp_server_connection = ServerConnection(HOST, PORT, username)
    temp_session = ChatSession(temp_server_connection, username, "register")

    key = RSA.generate(2048) #2048 bit key
    public_key = key.publickey().exportKey().decode()
    private_key = key.exportKey()
    cipher = AES.new(encryption_key.encode(), AES.MODE_EAX, nonce=remainder.encode()) #AES-256 encryption
    secure_private_key, tag = cipher.encrypt_and_digest(private_key)

    #send username, server_password, public_key, and secure_private_key to server
    temp_session.send_message(username)
    temp_session.send_message(public_key)
    temp_session.send_message(server_password)
    temp_session.send_message(b64encode(secure_private_key).decode())
    temp_session.send_message(b64encode(tag).decode())
    # while True:
    #     continue
    # temp_server_connection.sock.shutdown(socket.SHUT_WR)
    # temp_server_connection.sock.close()

def hash_password(password):
    h = SHA512.new()
    h.update(str.encode(password)) #convert string password to bytes, hash
    encryption_key = h.hexdigest()[:32] #use first 32 bytes as key
    remainder = h.hexdigest()[32:48] #use next 16 bytes to hold password on server
    server_password = h.hexdigest()[48:] #remainder, used as iv for encryption
    return encryption_key, server_password, remainder

# use usernmame and password to generate keys / do encryption
def login(username, password):
    encryption_key, server_password, remainder = hash_password(password)
    temp_server_connection = ServerConnection(HOST, PORT, username)
    temp_session = ChatSession(temp_server_connection, username, "login")

    temp_session.send_message(server_password)
    messages = []
    #second receive should receive 3 messages
    while len(messages) < 2:
        messages += temp_session.recv_messages()

    if messages[0].body != "valid":
        print("invalid password, try again")
        return True
    else:
        print("validated")
    public_key = messages[1].body
    secure_private_key = messages[2].body
    tag = messages[3].body
    cipher = AES.new(encryption_key.encode(), AES.MODE_EAX, nonce=remainder.encode()) #AES-256 encryption
    private_key = cipher.decrypt_and_verify(b64decode(secure_private_key.encode()), b64decode(tag.encode()))
    return False
    # temp_server_connection.sock.shutdown()
    # temp_server_connection.sock.close()


def query_login():
    username = input("Enter username:")
    password = getpass(prompt="Enter password:")
    return (username, password)

def valid_user(username):
    dest = input("Enter username of user you want to talk to or q to quit:")
    if dest == "q":
        return None
    temp_server_connection = ServerConnection(HOST, PORT, username)
    temp_session = ChatSession(temp_server_connection, username, "validate")

    temp_session.send_message(dest)
    messages = []
    #second receive should receive 3 messages
    while len(messages) < 1:
        messages += temp_session.recv_messages()

    if messages[0].body == "invalid user":
        print("This user does not exist, please try again")
        return None

    # other users public key, used for decrypting messages in end to end encryption
    dest_public_key = messages[0].body
    return dest

import socket

def connect_To_Server():
    HOST = socket.gethostname()  # For testing we will use same machine
    PORT = 12345  # Arbitrary port for connecting
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def send_Message_to_server(message, server_socket):
    encoded = str.encode(message)
    server_socket.sendall(encoded)
    data = server_socket.recv(1024)
    decoded = data.decode("utf-8")
    return decoded

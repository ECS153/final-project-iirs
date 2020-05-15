#!/usr/bin/env python3

import socket

HOST = socket.gethostname() # For testing we will use same machine
PORT = 12345 # Arbitrary port for connecting

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    sending_Str = 'Test Test'
    print("Sending: " + sending_Str)
    encoded = str.encode(sending_Str)
    s.sendall(encoded)
    data = s.recv(1024)

print('Received', repr(data))
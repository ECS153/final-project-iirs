# Basic server implementation
# Server expects messages in format:
# $SourceID[len 1]$DestID[len 1]$Mode[R or X]$Message

"""
Todo:
- Convert server to accept multiple connections on multiple rounds
    - Non blocking, will use selectors, automatic connection management
    - Selector uses single thread multitasking which is fine for this
- Ensure the temp buffers and sending rounds work

How server could work for our first test (could be different once multi-connection):
- Connect to source client, send any waiting data, accept any new data
- Store new data in buffer, close.
- Once dest client connects, send any data waiting for him, etc. Same process.
"""

import socket, ssl
from threading import Thread

HOST = socket.gethostname() # For testing we will use same machine
PORT = 12345 # Arbitrary port for connecting
MSG_SIZE = 4096 # Size of the message sent / received

clients = {} # holds all the active clients

def server():
    # Create the socket instance and bind the host + port
    main_socket = socket.socket()
    main_socket.bind((HOST,PORT))

    # Listen for connection and accept, printing the status
    main_socket.listen()
    conn, addr = main_socket.accept()
    print("[Server] Connected to " + str(addr))

    # Temporary buffers to store messages to 1 or 2.
    # This will be eventually unecessary with deadrops
    to_usr1 = []
    to_usr2 = []

    while True:
        # Get 4096 byes of data from client
        data = conn.recv(MSG_SIZE).decode()
        if not data:
            break # If we got nothing, then break
        data_str = str(data)
        print("Got data: " + data_str)

        # Decode the header
        source_client = data_str[0:1] # The "address" of source client
        dest_client = data_str[2:3] #  The "address" of dest client
        client_mode = data_str[4:5] # The mode in which client is (R, X)
        # Note: R = read, X = read + write

        print(source_client,dest_client,client_mode)

        # Check for pending messages and send
        data_send = " "
        if source_client == "1" and to_usr1:
            print("Checking 1's buffer")
            data_send = to_usr1.pop()
        elif source_client == "2" and to_usr2:
            print("Checking 2's buffer")
            data_send = to_usr2.pop()

        # Send data back to source client
        print("[Server] Sending data: " + data_send)
        conn.sendall(data_send.encode())

        # If we are in read/write mode then store any sent data
        if client_mode == "X":
            print("We are in read/write mode")
            if dest_client == "1":
                to_usr1.append(data_str[7:])
                print("Wrote to 1's buffer")
            elif dest_client == "2":
                to_usr2.append(data_str[7:])
                print("Wrote to 2's buffer")
            else:
                print("Error, incorrect format.")
                return

    # Close the connection
    conn.close()

def accept_connection(server):
    while True:
        client, addr = server.accept()
        print("connected")
        clients[client] = addr
        Thread(target=client_thread, args=(client)).start()

def client_thread(client):
    while True:
        try:
            data = client.recv(MSG_SIZE).decode()
            if not data:
                continue
                #remove(conn)
            else:
                send_message(data)

        except:
            continue

def decode_data(data):
    # Decode the header
    source_client = data[1:2] # The "address" of source client
    dest_client = data[3:4] #  The "address" of dest client
    client_mode = data[5:6] # The mode in which client is (R, X)
    # Note: R = read, X = read + write
    message = data[7:]
    return source_client, dest_client, client_mode, message

def send_message(data):
    src, dest, mode, message = decode_data(str(data))
    if not src in clients or not dest in clients:
        print("invalid src: " + src + " or dest: " + dest)
        return
    for client, addr in clients.items():
        if dest == addr:
            client.sendall(message.encode())


def server_test():
    # Create the socket instance and bind the host + port
    main_socket = socket.socket()
    main_socket.bind((HOST,PORT))

    # Listen for connection and accept, printing the status
    main_socket.listen()
    conn, addr = main_socket.accept()
    print("[Server] Connected to " + str(addr))
    while True:
        # Get 4096 byes of data from client
        data = conn.recv(MSG_SIZE).decode()
        if not data:
            break # If we got nothing, then break
        data_str = str(data)
        print("Got data: " + data_str)


        # Send data back to source client
        print("[Server] Sending data: " + data_str)
        conn.sendall(data_str.encode())

    # Close the connection
    conn.close()

def setup_server():
    main_socket = socket.socket()
    main_socket.bind((HOST,PORT))

    # Listen for connection and accept, printing the status
    main_socket.listen()
    conn, addr = main_socket.accept()
    print("[Server] Connected to " + str(addr))
    return main_socket

if __name__ == "__main__":
#    server = setup_server()
#    connection_thread = Thread(target=accept_connection, args=(server,)).start()
#    connection_thread.join()
#    server.close()
    server_test()

# Basic server implementation
# Server expects messages in format $SourceID$DestID$Message

"""
Todo:
- Convert server to accept multiple connections on multiple rounds
    - Non blocking, will use selectors, automatic connection management
    - Selector uses single thread multitasking which is fine for this
- Ensure the temp buffers and sending rounds work

How server could work for our first test (could be slightly different. 
it's set up differently for initial skeleton code. easy to change order):
- Connect to source client, send any waiting data, accept any new data
- Store new data in buffer, close.
- Once dest client connects, send any data waiting for him, etc. Same process.
"""

import socket, ssl

HOST = socket.gethostname() # For testing we will use same machine
PORT = 12345 # Arbitrary port for connecting

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
    to_usr1 = ["goodbye"]
    to_usr2 = []

    while True:
        # Get 4096 byes of data from client
        data = conn.recv(4096).decode()
        if not data: 
            break # If we got nothing, then break
        data_str = str(data)
        print("Got data: " + data_str)
        
        # Check who the client is, store data, and set up any queued data to send
        if data_str[0:2] == "$1":
            to_usr2.append(data)
            if to_usr1:
                data = to_usr1.pop()
            else:
                break
        elif data_str[0:2] == "$2":
            to_usr1.append(data)
            if to_usr2:
                data = to_usr2.pop()
            else:
                break
        else:
            break

        # Send the waiting data to client
        print("[Server] Sending data to client")
        conn.send(data.encode())
    # Close the connection
    conn.close()


if __name__ == "__main__":
    server()
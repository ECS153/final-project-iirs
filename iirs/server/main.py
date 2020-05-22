# Basic multi-client server implementation
# Server expects messages in format:
# $SourceID[len 1]$DestID[len 1]$Mode[R or X]$Message


import socket, ssl
from threading import Thread
from socketserver import ThreadingMixIn

HOST = socket.gethostname() # For testing we will use same machine
PORT = 12345 # Arbitrary port for connecting
MSG_SIZE = 4096 # Size of the message sent / received

# Temporary buffers to store messages to 1 or 2.
# This will be eventually unecessary with deadrops
to_usr1 = []
to_usr2 = []

class ConnectionThread(Thread): 
    def __init__(self,host,port,conn): 
        Thread.__init__(self) 
        self.host = host
        self.port = port
        self.conn = conn
        self.hpstring = str(host) + ":" + str(port)
        print("[Server] Client connected at", self.hpstring)
    
    def decode(self, data_str):
        # Decode the header
        source_client = data_str[1] # The "address" of source client_script
        dest_client = data_str[3] #  The "address" of dest client_script
        client_mode = data_str[5] # The mode in which client_script is (R, X)
        # Note: R = read, X = read + write
        return source_client, dest_client, client_mode
    
    def get_messages(self, source_client):
        data_send = " "
        if source_client == "1" and to_usr1:
            data_send = to_usr1.pop()
        elif source_client == "2" and to_usr2:
            data_send = to_usr2.pop()
        return data_send
    
    def send_messages(self, msg):
        self.conn.sendall(msg.encode())
    
    def store_messages(self, dest_client, data_str):
        if dest_client == "1":
            to_usr1.append(data_str[7:])
            #print("[Server] Wrote to 1's buffer")
        elif dest_client == "2":
            to_usr2.append(data_str[7:])
            #print("[Server] Wrote to 2's buffer")
        else:
            print("[Server] Error, incorrect message format")
            return
 
    def run(self): 
        while True : 
            data = self.conn.recv(MSG_SIZE).decode()
            if not data:
                print("[Server] Client " + self.hpstring + " has disconnected!", flush=True)
                return
            data_str = str(data)
            print ("[Server] Received data from" + self.hpstring + ": " + data_str)

            # Decode data
            source_client, dest_client, client_mode = self.decode(data_str)
            # Check for messages 
            data_send = self.get_messages(source_client)
            print("[Server] Data sent to " + self.hpstring + " : " + data_send)
            # Send messages 
            self.send_messages(data_send)
            # Store messages
            if client_mode == "X":
                self.store_messages(dest_client, data_str)

def main():
    # Set up connection and client list
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    main_socket.bind((HOST,PORT))
    clients = []
    print("[Server] Server started at " + str(HOST) + ":" + str(PORT))
    
    # Keep accepting connections from clients
    while True:
        main_socket.listen()
        conn, (host, port) = main_socket.accept()
        connection_thread = ConnectionThread(host,port,conn)
        connection_thread.start()
        clients.append(connection_thread)
    for thread in clients:
        thread.join()

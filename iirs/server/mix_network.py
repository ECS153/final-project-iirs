import socket, ssl
from .main import ConnectionThread, DeadDrop
from threading import Thread
import random
import threading, time


class MixNetwork:
    def __init__(self, deadDrop):
        self.deadDrop = deadDrop
        self.HOST = socket.gethostname()  # For testing we will use same machine
        self.PORT = 12345  # Arbitrary port for connecting
        self.MSG_SIZE = 4096  # Size of the message sent / received
        # Set up connection and client list
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.main_socket.bind((self.HOST, self.PORT))


        self.incoming_message_queue = []
        self.outgoing_message_queue = []
        self.clients = []
        self.swaps = []

        print("[Server] Server started at " + str(self.HOST) + ":" + str(self.PORT))

    def listen(self):
        # Keep accepting connections from clients
        self.main_socket.listen()
        conn, (host, port) = self.main_socket.accept()
        connection_thread = ConnectionThread(host, port, conn, self.incoming_message_queue)
        connection_thread.start()
        self.clients.append(connection_thread)
        for thread in self.clients:
            thread.join()

    def mix_and_pass(self):
        if len(self.incoming_message_queue) > 2:
            self.mixing()
            self.outgoing_message_queue = self.deadDrop.handle_messages()
            self.reverse_mix()
        threading.Timer(2, self.mix_and_pass).start()


    def mixing(self):
        # we will be generating the key each round
        key = random.randint(1, 1000)
        random.seed(key)
        randomNum = random.randint(1, 1000)
        self.swaps = []

        # Fisher–Yates shuffle
        for i in range(len(self.incoming_message_queue) - 1, 0, -1):
            if i == 0:
                break
            j = randomNum % i
            self.incoming_message_queue = self.swap_two_elements(i, j, self.incoming_message_queue)
            self.swaps.append((i, j))

    def reverse_mix(self):
        reversed_swaps = self.swaps.reverse()
        for swap in reversed_swaps:
            self.outgoing_message_queue = self.swap_two_elements(swap[0], swap[1], self.outgoing_message_queue)

    def swap_two_elements(self, index_a, index_b, array):
        temp = array[index_a]
        array[index_a] = array[index_b]
        array[index_b] = temp
        return array












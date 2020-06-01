import socket, ssl
from .connectionThread import *
from threading import Thread
import random
import threading, time
from .deaddrop import *
from ..message import *
from apscheduler.schedulers.background import BackgroundScheduler


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

        key = rsa.generate_private_key(65537, 2048, default_backend())
        certificate = x509.CertificateBuilder(x509.Name([]), x509.Name([]), key.public_key(), x509.random_serial_number(), datetime.datetime.utcnow(), datetime.datetime.utcnow() + datetime.timedelta(days=7)).sign(key, hashes.SHA256(), default_backend())
        with NamedTemporaryFile() as certfile, NamedTemporaryFile() as keyfile:
            keyfile.write(key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()))
            certfile.write(certificate.public_bytes(Encoding.PEM))
            keyfile.flush()
            certfile.flush()
            self.main_socket_ssl = ssl.wrap_socket(self.main_socket, server_side=True, certfile=certfile.name, keyfile=keyfile.name)


        self.incoming_message_queue = {}
        self.outgoing_message_queue = {}
        self.shuffled_messages = []
        self.src_arr = []
        self.clients = []
        self.swaps = []

        sched = BackgroundScheduler()
        # job is a cron style job, running every second
        sched.add_job(self.mix_and_pass, 'cron', second='*')
        sched.start()

        print("[Server] Server started at " + str(self.HOST) + ":" + str(self.PORT))

    def listen(self):
        self.main_socket_ssl.listen()
        conn, (host, port) = self.main_socket_ssl.accept()
        connection_thread = ConnectionThread(host, port, conn, self.incoming_message_queue, self.outgoing_message_queue)
        connection_thread.start()
        self.clients.append(connection_thread)


    def mix_and_pass(self):
        swaps = []
        src_arr = []
        shuffled_messages = []
        print("mix_and_pass")
        # Delete all dead threads
        # This basically goes through the clients list and make sure all dead threads are deleted
        for connection in self.clients:
            if not connection.isAlive():
                print("MixNPAss: Deleting dead thread") # Debug 'Prints when Dead thread is deleted'
                self.clients.remove(connection)
                connection.join()
        if len(self.incoming_message_queue.keys()) > 1:
            swaps, src_arr, shuffled_messages = self.mixing(swaps, src_arr, shuffled_messages)
            response_shuffled = self.deadDrop.handle_messages(shuffled_messages)
            self.reverse_mix(response_shuffled, swaps, src_arr)
            for connection in self.clients:
                if connection.isAlive():
                    print("MixNPass: trying to send for conn:",connection) # Debug 'Prints when mixnet is trying to send for a thread'
                    connection.get_messages()




    def mixing(self, swaps, src_arr, shuffled_messages):
        # we will be generating the key each round
        key = random.randint(1, 1000)
        random.seed(key)
        randomNum = random.randint(1, 1000)
        for key in self.incoming_message_queue.keys():
            src_arr.append(key)
            #src_arr[index] = key
            # should only be one message each round
            old_message = self.incoming_message_queue[key][0]
            #new_message = Message(None, old_message.dest, old_message.body)
            new_message = Message(None, '1', old_message.body) # this is temporary
            shuffled_messages.append(new_message)

        # Fisher–Yates shuffle
        for i in range(len(shuffled_messages) - 1, 0, -1):
            if i == 0:
                break
            j = randomNum % i
            shuffled_messages = self.swap_two_elements(i, j, shuffled_messages)
            swaps.append((i, j))
        return swaps, src_arr, shuffled_messages

    def reverse_mix(self, response_shuffled, swaps, src_arr):
        swaps.reverse()
        for swap in swaps:
            response_shuffled = self.swap_two_elements(swap[0], swap[1], response_shuffled)
        i = 0
        for message in response_shuffled:
           self.outgoing_message_queue[src_arr[i]] = Message(None, src_arr[i], message)

    def swap_two_elements(self, index_a, index_b, array):
        temp = array[index_a]
        array[index_a] = array[index_b]
        array[index_b] = temp
        return array















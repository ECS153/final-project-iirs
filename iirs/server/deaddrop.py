# Deaddrop implementation for the server

from ..message import Message
import time
from typing import List
from threading import Thread

# Global expire limit till figure out what to do with messages
EXPIRE_LIMIT = 0 # seconds past commit to deaddrop (keep at 0 for [BETA 2] Solution)
# Global frequency that the garbage collector will run at
COLLECT_FREQ = 1 # seconds

# Deaddrop Message Wrapper Object
class DeaddropMessage:
    def __init__(self, message: Message):
        # Set the time stamp and store the message
        self.timestamp = int(time.time())
        self.data = message

# Main Deaddrop Object
class DeadDrop:
    def __init__(self):
        # Create an empty list for storage
        self.data = []
    
    def insert(self, message):
        # Inserts a message into the deaddrop
        self.data.append(DeaddropMessage(message))
    
    def get(self):
        # Returns all the messages within the current deaddrop
        raw_data = []
        # Remove DeaddropMessage class wrapper
        for block in self.data:
            raw_data.append(block.data)
        return raw_data
    
    def delete(self):
        # Deletes all expired messages within a deaddrop
        old_len = len(self.data)
        cur_time = int(time.time())
        self.data = [x for x in self.data if ((cur_time - x.timestamp) < EXPIRE_LIMIT)]       

class GarbageCollector(Thread):
    def __init__(self, deaddrops):
        Thread.__init__(self)
        self.dd = deaddrops
    def run(self):
        while True:
            print("Running garbage collector...")
            for deaddrop in self.dd.values():
                deaddrop.delete()
            time.sleep(COLLECT_FREQ)            

# Holds and manages deaddrops
class DeaddropManager:
    def __init__(self, num):
        # Set up 'num' deaddrops and automatic garbage collection
        self.dd = {}
        self.num = num
        for i in range(1,num + 1):
            self.dd[str(i)] = DeadDrop()
        
        # [BETA 1] Start garbage collection (Implemented and working but not turning this on until needed)
        # (We will be attempting to delete upon every round)
        #gc = GarbageCollector(self.dd)
        #gc.start()

    def __store(self, messages: List[Message]):
        # Stores a set of data into their respective deaddrops
        # Returns a list of data blocks that were not handled, and the contents of deaddrops
        failures = []
        store_order = []
        for msg in messages:
            try:
                # Get message dest, store in DD, return the order of deaddrops
                cur_key = msg.dest
                self.dd[cur_key].insert(msg)
                store_order.append(cur_key)
            except KeyError:
                print("[Server] Deaddrop storage error. Invalid key.")
                print("Offending message:", msg.body)
                failures.append(msg)

        return failures,store_order
    
    def __get(self, ids: List[str]):
        # Gets all the messages in the deaddrops provided in ids and returns
        ret_data = []
        for i in ids:
            try: 
                ret_data.append(self.dd[i].get())
            except KeyError:
                print("[Server] Deaddrop extraction error. Invalid key.")
                print("Offending key:", i)
        # [BETA 2] Once we get all deaddrops, delete the data
        for i in self.dd.values():
            i.delete()
        # Returns an empty list if no messages to send
        return ret_data

    def handle_messages(self, messages):
        # Store the messages recieved
        not_stored, store_order = self.__store(messages)
        # Get the contents of the deaddrops and put in list
        retrieved_messages = self.__get(store_order)
        return retrieved_messages

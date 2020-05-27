from.message import *
# Deaddrop implementation for the server

# Holds and manages deaddrops
class DeaddropManager:
    def __init__(self, num):
        # Initialization code will go here
        # Set up 'num' deaddrops and automatic garbage collection
        self.dd = {}
        self.num = num
        for i in range(1,num + 1):
            self.dd[str(i)] = DeadDrop()
        
        # Implement garbage collection + initialization

    #message here is of the message class
    def store(self, messages):

        ret_data = []
        # Stores a set of data into their respective deaddrops
        # Returns a list of data blocks that were not able to be saved
        for message in messages:
            message.set_drop_box_id()
            # store payload of the message
        return ret_data, messages
    
    def get(self, messages):
        ret_data = []
        # Returns all the contents of a certain deaddrop.
        # Returns an empty list if empty or not found.
        for message in messages:
            message.get_drop_box_id()
            # retrieve messages in from the corresponding dead drop
            # fill in the payload with the data
        return ret_data, messages

    # a high level idea of how the dead drop should interact with the mix net
    def handle_messages(self, messages):
        # store the message where they belong
        stored_messages = self.store(messages)
        # now retrieve messages
        retrieved_messages = self.get(stored_messages)

        return retrieved_messages

# Main class to be used for deaddrop objects
class DeadDrop:
    def __init__(self):
        # Initialization code will go here
        pass
    
    def insert(self, message):
        # Inserts a message into the deaddrop
        pass
    
    def get(self):
        # Returns all the messages within the current deaddrop
        pass
    
    def delete(self):
        # Deletes all expired messages within a deaddrop
        pass

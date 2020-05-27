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
    
    def store(self, data):
        ret_data = []
        # Stores a set of data into their respective deaddrops
        # Returns a list of data blocks that were not able to be saved
        return ret_data
    
    def get(self, id):
        ret_data = []
        # Returns all the contents of a certain deaddrop.
        # Returns an empty list if empty or not found.
        return ret_data

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

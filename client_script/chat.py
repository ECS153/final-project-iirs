from threading import Thread
from abc import ABC, abstractmethod

# A channel with another user, abstracting lower level network details
# Does not include end to end encryption
class UserChannel(ABC):
    @abstractmethod
    def send(self, data):
        pass

    @abstractmethod
    def recv(self):
        pass

# An end to end encrypted session with another user
class ChatSession:
    def __init__(self, user_channel):
        self.user_channel = user_channel

    def send_message(self, msg):
        # TODO encrypt with other user's public key; send over channel
        pass

    def recv_message(self):
        # TODO verify sender signature and decrypt
        pass

def RecieveThread(Thread):
    def __init__(self, chat_session):
        super().__init__(self)
        self.chat_session = chat_session

    def run(self):
        while True:
            msg = self.chat_session.recv_message()
            # TODO What should it do? Print directly? Send to UI thread?

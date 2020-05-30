

from .mix_network import MixNetwork
from .deaddrop import *

def main():
    dead_drop = DeaddropManager(1)
    mix_net = MixNetwork(dead_drop)
    while True:
        print("in while true loop")
        mix_net.listen()
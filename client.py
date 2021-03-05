from network import Network
from engine import Engine
import sys
import threading

def delete_last_line(): #delete the last line in the STDOUT
    sys.stdout.write('\x1b[1A') #cursor up one line
    sys.stdout.write('\x1b[2K') #delete last line


class Client():
    def __init__(self, name=None):
        if name is None: self.name = input("What's your name? ")
        else: self.name = name
        self.create_connection()

    def create_connection(self):
        self.n = Network()
        self.p = Engine(name=self.name)    #instantiate the player upon first join
        self.n.send(self.p) #first handshake (to send basic player info)
        threading.Thread(target=self.receive_message, args=()).start()
        threading.Thread(target=self.input_message, args=()).start()

    def receive_message(self):
        while True:
            p = self.n.receive()
            if type(p)==Engine:
                p.display()
            else:
                print(p)

    def input_message(self):
        while True:
            self.p.input_text(input("🟢 "))
            self.n.send(self.p)

# client = Client()
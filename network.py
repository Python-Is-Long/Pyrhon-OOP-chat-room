# 2021-1-25
import socket
import pickle
import time

class Network:
    def __init__(self, server="10.0.0.142", port=5555, packet_size=2048):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.address = (self.server, self.port)
        self.packet_size = packet_size
        print(f"Connecting to {server}:{port}")
        self.connect()

    def connect(self, retry=1):
        while True:
            try:
                self.client.connect(self.address)
                print("✔ Connected to server")
                break
            except:
                print(f"❌ Couldn't connect to server, retrying in {retry} s...")
                time.sleep(retry)

    def send(self, data):
        try:
            # print("sending")
            self.client.send(pickle.dumps(data))
            # print("sent")
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return pickle.loads(self.client.recv(self.packet_size))
        except socket.error as e:
            print(e)
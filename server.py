# 2021-1-25
import socket
import threading
import pickle
import requests
from engine import Engine

def get_external_IP():
    return requests.get('https://api.ipify.org').text

class Server():
    def __init__(self, IP_address="external", Port=5555, packet_size=2048):
        self.host_name = socket.gethostname()
        print(self.host_name)
        if IP_address.lower()=="external":
            self.IP_address = get_external_IP()
        elif IP_address.lower()=="internal":
            self.IP_address = socket.gethostbyname(self.host_name)
        else:
            self.IP_address = IP_address

        self.Port = Port
        print(f"Server IP: {self.IP_address}, Port: {self.Port}")
        self.packet_size=packet_size
        self.start_server()
    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: self.s.bind((self.IP_address, self.Port))
        except socket.error as e: str(e)
        self.s.listen()  # a number here will limit the number of connections 
        print(">>> Server Started! Waiting for a connection...")
        self.clients = []
        self.usernames = {}
        self.currentID = 0
        while True:
            connection, address = self.s.accept()  # connection is the socket object for the user; address is the IP address of the client that just connected
            print(f"Connected to: {address}, ID: {self.currentID}")
            try:
                data = pickle.loads(connection.recv(self.packet_size))
                username = data.name
                self.usernames[connection] = username
                print(f"{username} has joined the chat.")
                self.broadcast(f"{username} has joined the chat.")
                self.clients.append(connection)  # append the client to a list for easy broadcasting
                threading.Thread(target=self.handle_client, args=(connection, self.currentID)).start()  # create an individual thread for every user that connects
                self.currentID += 1
            except:
                print("Client connection failed")


    def handle_client(self, conn, ID):
        while True:
            try:
                data = pickle.loads(conn.recv(self.packet_size))
                print(f"Received: {data} from ID: {ID}")
                data.ID = ID
                data.time_stamp()
                self.broadcast(pickle.dumps(data))  # send the updated info to all except self
                print(f"Sent: {data} to everyone")
            except:
                conn.close() #conn.shutdown(socket.SHUT_RDWR)
                self.clients.remove(conn)  # Removes the object from the list that was created at the beginning of the program
                print(f"{self.usernames[conn]} has left the chat.")
                self.broadcast(f"{self.usernames[conn]} has left the chat.")
                break
        print(f"Lost connection to ID: {ID}")
        conn.close()


    def broadcast(self, data, exclude_connections=[]):  # broadcast the data to all clients with an option to exclude the one sending the data
        if type(data) == str: data=pickle.dumps(data)
        if type(exclude_connections) != list: exclude_connections = [exclude_connections]
        for client in self.clients:
            if client not in exclude_connections:
                client.send(data)

server = Server("internal")
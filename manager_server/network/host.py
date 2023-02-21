import socket
import threading
from manager_server.network.client import Client
from manager_server.database.database import Database


class Host:
    def __init__(self, database: Database):
        self.database = database
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.bind(("0.0.0.0", 1589))
        self.sock.listen(50)
        self.sock.setblocking(True)

    def accept_client(self, sock: socket.socket):
        client = Client(sock, self.database)
        client.loop()

    def loop(self):
        while True:
            client, addr = self.sock.accept()
            thread = threading.Thread(target=lambda: self.accept_client(client))
            thread.start()

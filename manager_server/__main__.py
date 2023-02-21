from manager_server.network.host import Host
from manager_server.database.database import Database

db = Database("passwords.db")

sock = Host(db)
sock.start()

while True:
    sock.loop()

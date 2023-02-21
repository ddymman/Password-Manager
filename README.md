`README file is not fullfiled___README file is not fullfiled___README file is not fullfiled`
# Prerequisites

* Python 3.10
* pillow
* tkinter
* cryptography

Installing prerequisites:
`pip install pillow cryptography`

# Launching

To start the server run
`start_server.bat` if you are on windows, and `start_server.sh` if you are on linux/macos.

To start the client run `start_client.bat` if you are on windows, and `start_client.sh` if you are on linux/macos.

# Configuration

The client is configured to connect to localhost server by default, this can be changed in `manager_client/__main__.py`

The server stores the database in the current working directory by default, this can be changed in `manager_server/__main__.py`

# Architecture

The code uses a monorepo architecture to share some code between the server and the client.

This allows for easier and more bug-free development of networking code, because it is all contained in one place.

This also enables for easier client/server changes testing without the need to update git submodules.

Server uses a multithreaded architecture where a thread is allocated for each client.

Client uses a dual-thread architecture, where main thread is running the gui, and background thread is running the network communication.

Shared network code is located in `manager_network`, networking code for server is inside `manager_server/network`, networking code for client is inside `manager_client/network`

# Encryption

Password encryption is done client-side and unencrypted passwords never leave the client, Fernet encryption with PBKDF2HMAC key derivation function are used.
Crypto details are inside `manager_client/crypto/crypto.py`

Server-side only receives encrypted passwords, the user account password is hashed on the client-side, and salted on server-side before writing to the database.
This protects against rainbow-table attacks and makes similar passwords have completely different hashes.

import socket
import json
import os
import hashlib
from manager_network.register import RegisterMessage, RegisterResponseCode, RegisterResponseMessage
from manager_network.login import LoginMessage, LoginResponseCode, LoginResponseMessage
from manager_network.passwords import GetPasswordsResponseCode, GetPasswordsResponseMessage, Password, \
    AddPasswordMessage, AddPasswordResponseMessage, AddPasswordResponseCode, DeletePasswordMessage, \
    DeleteAllPasswordsMessage
from manager_network.messagedata import NetworkMessage, MessageType
from manager_server.database.database import Database
from manager_server.database.account import Account, AccountCreationResult
from manager_server.database.password import Password as DatabasePassword


class Client:
    def __init__(self, sock: socket.socket, database: Database):
        self.sock = sock
        self.account = None
        self.database = database

    def send(self, message: NetworkMessage):
        data = json.dumps(message.to_json())
        # every packet has a 4 byte length before the packet, to tell the client exactly how much to read
        self.sock.send(len(data).to_bytes(4, 'little'))
        self.sock.send(data.encode())

    def on_register(self, message: NetworkMessage):
        register_message = RegisterMessage.from_json(json.loads(message.data))

        # salt the password hash to protect against rainbow-table attacks
        salt = os.urandom(32)
        salted_hash = hashlib.pbkdf2_hmac("sha256", bytes.fromhex(register_message.password), salt, 480000)

        # insert account into database
        account = Account(0, register_message.username, salted_hash.hex() + ":" + salt.hex())
        result = account.insert(self.database)

        # Convert database response code to network response code
        network_result = RegisterResponseCode.SUCCESS

        if result == AccountCreationResult.EXISTS:
            network_result = RegisterResponseCode.EXISTS
        elif result == AccountCreationResult.OK:
            network_result = RegisterResponseCode.SUCCESS

        self.account = account
        register_response = RegisterResponseMessage(network_result)
        network_response = NetworkMessage(message.message_id, register_response.message_type(),
                                          json.dumps(register_response.to_json()))

        self.send(network_response)

    def on_login(self, message: NetworkMessage):
        login_message = LoginMessage.from_json(json.loads(message.data))

        account = Account.find(self.database, login_message.username)
        if account is None:
            login_response = LoginResponseMessage(LoginResponseCode.NO_ACCOUNT)
            self.send(NetworkMessage(message.message_id, login_response.message_type(),
                                     json.dumps(login_response.to_json())))
            return

        # get the password from the database, salt the client hash and check equality
        split_pass = account.password.split(":")
        salt = bytes.fromhex(split_pass[1])
        salted_hash = hashlib.pbkdf2_hmac("sha256", bytes.fromhex(login_message.password), salt, 480000)

        if salted_hash.hex() != split_pass[0]:
            login_response = LoginResponseMessage(LoginResponseCode.INVALID_PASSWORD)
            self.send(NetworkMessage(message.message_id, login_response.message_type(),
                                     json.dumps(login_response.to_json())))
            return

        self.account = account
        login_response = LoginResponseMessage(LoginResponseCode.SUCCESS)
        self.send(NetworkMessage(message.message_id, login_response.message_type(),
                                 json.dumps(login_response.to_json())))

    def get_passwords(self, message: NetworkMessage):
        # authorization check
        if self.account is None:
            password_response = GetPasswordsResponseMessage(GetPasswordsResponseCode.UNAUTHORIZED, [])
            self.send(NetworkMessage(message.message_id, password_response.message_type(),
                                     json.dumps(password_response.to_json())))
            return

        # get all passwords for the current authorized client, and remap them from database model to network model
        passwords = list(map(lambda e: Password(e.id, e.username, e.password, e.website),
                             DatabasePassword.get_passwords(self.account.id, self.database)))

        password_response = GetPasswordsResponseMessage(GetPasswordsResponseCode.SUCCESS, passwords)
        self.send(NetworkMessage(message.message_id, password_response.message_type(),
                                 json.dumps(password_response.to_json())))

    def add_password(self, message: NetworkMessage):
        if self.account is None:
            add_response = AddPasswordResponseMessage(AddPasswordResponseCode.UNAUTHORIZED)
            self.send(
                NetworkMessage(message.message_id, add_response.message_type(), json.dumps(add_response.to_json())))
            return

        add_message = AddPasswordMessage.from_json(json.loads(message.data))

        DatabasePassword(0, self.account.id, add_message.password.username, add_message.password.password,
                         add_message.password.website).insert(self.database)

        add_response = AddPasswordResponseMessage(AddPasswordResponseCode.SUCCESS)
        self.send(NetworkMessage(message.message_id, add_response.message_type(), json.dumps(add_response.to_json())))

    def delete_password(self, message: NetworkMessage):
        if self.account is None:
            return

        delete_message = DeletePasswordMessage.from_json(json.loads(message.data))

        DatabasePassword(delete_message.id, self.account.id, "", "", "").delete(self.database)

    def delete_all_passwords(self, message: NetworkMessage):
        if self.account is None:
            return

        DatabasePassword(0, self.account.id, "", "", "").delete_all(self.database)

    # main packet handler, returns if the thread should continue running
    def on_packet(self) -> bool:
        # receive packet length and get the full packet
        data_len = int.from_bytes(self.sock.recv(4), "little")
        data = self.sock.recv(data_len)

        if data_len == 0 or len(data) == 0:
            return False

        # decode it into basic NetworkMessage without actually looking at data
        message_data = json.loads(data.decode())
        network_message = NetworkMessage.from_json(message_data)

        # data-specific packet message handlers
        if network_message.message_type() == MessageType.REGISTER.value:
            self.on_register(network_message)
        elif network_message.message_type() == MessageType.LOGIN.value:
            self.on_login(network_message)
        elif network_message.message_type() == MessageType.GET_PASSWORDS.value:
            self.get_passwords(network_message)
        elif network_message.message_type() == MessageType.ADD_PASSWORD.value:
            self.add_password(network_message)
        elif network_message.message_type() == MessageType.DELETE_PASSWORD.value:
            self.delete_password(network_message)
        elif network_message.message_type() == MessageType.DELETE_ALL_PASSWORDS.value:
            self.delete_all_passwords(network_message)

        return True

    def loop(self):
        # loop until the client has a connection error, when that happens the thread dies
        try:
            while True:
                if not self.on_packet():
                    break
        except ConnectionError:
            pass

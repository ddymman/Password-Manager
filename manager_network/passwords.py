from typing import List

import json
from manager_network.messagedata import MessageData, RPCMessage, MessageType
from enum import Enum


class Password:
    id: int
    username: str
    password: str
    website: str

    def __init__(self, id: int, username: str, password: str, website: str):
        self.id = id
        self.username = username
        self.password = password
        self.website = website

    def from_json(json: dict):
        return Password(json["id"], json["username"], json["password"], json["website"])

    def to_json(self) -> dict:
        json = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "website": self.website
        }
        return json


class GetPasswordsResponseCode(Enum):
    SUCCESS = 0
    UNAUTHORIZED = 1


class GetPasswordsResponseMessage(MessageData):
    def __init__(self, code: GetPasswordsResponseCode, passwords: List[Password]):
        self.code = code
        self.passwords = passwords

    def from_json(j: dict):
        passwords = list(map(lambda e: Password.from_json(e), j["passwords"]))
        return GetPasswordsResponseMessage(j["code"], passwords)

    def to_json(self) -> dict:
        json = {
            "code": self.code.value,
            "passwords": list(map(lambda e: e.to_json(), self.passwords))
        }
        return json

    def message_type(self) -> int:
        return MessageType.GET_PASSWORDS_RESPONSE.value


class GetPasswordsMessage(RPCMessage):
    def __init__(self):
        pass

    def from_json(json: dict):
        return GetPasswordsMessage()

    def to_json(self) -> dict:
        return {}

    def message_type(self) -> int:
        return MessageType.GET_PASSWORDS.value

    def response_from_json(self, json: dict):
        return GetPasswordsResponseMessage.from_json(json)


class AddPasswordResponseCode(Enum):
    SUCCESS = 0
    UNAUTHORIZED = 1


class AddPasswordResponseMessage(MessageData):
    def __init__(self, code: AddPasswordResponseCode):
        self.code = code

    def from_json(j: dict):
        return AddPasswordResponseMessage(j["code"])

    def to_json(self) -> dict:
        json = {
            "code": self.code.value
        }
        return json

    def message_type(self) -> int:
        return MessageType.ADD_PASSWORD_RESPONSE.value


class AddPasswordMessage(RPCMessage):
    def __init__(self, password: Password):
        self.password = password

    def from_json(json: dict):
        return AddPasswordMessage(Password.from_json(json["password"]))

    def to_json(self) -> dict:
        j = {
            "password": self.password.to_json()
        }
        return j

    def message_type(self) -> int:
        return MessageType.ADD_PASSWORD.value

    def response_from_json(self, json: dict):
        return AddPasswordResponseMessage.from_json(json)


class DeletePasswordMessage(MessageData):
    def __init__(self, id: int):
        self.id = id

    def from_json(json: dict):
        return DeletePasswordMessage(json["id"])

    def to_json(self) -> dict:
        j = {
            "id": self.id
        }
        return j

    def message_type(self) -> int:
        return MessageType.DELETE_PASSWORD.value


class DeleteAllPasswordsMessage(MessageData):
    def __init__(self):
        pass

    def from_json(json: dict):
        return DeleteAllPasswordsMessage()

    def to_json(self) -> dict:
        return {}

    def message_type(self) -> int:
        return MessageType.DELETE_ALL_PASSWORDS.value

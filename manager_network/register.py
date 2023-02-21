from manager_network.messagedata import MessageData, RPCMessage, MessageType
from enum import Enum


class RegisterResponseCode(Enum):
    SUCCESS = 0
    EXISTS = 1


class RegisterResponseMessage(MessageData):
    def __init__(self, code: RegisterResponseCode):
        self.code = code

    def from_json(json: dict):
        return RegisterResponseMessage(json["code"])

    def to_json(self) -> dict:
        json = {
            "code": self.code.value
        }
        return json

    def message_type(self) -> int:
        return MessageType.REGISTER_RESPONSE.value


class RegisterMessage(RPCMessage):
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def from_json(json: dict):
        return RegisterMessage(json.get("username"), json.get("password"))

    def to_json(self) -> dict:
        json = {
            "username": self.username,
            "password": self.password
        }
        return json

    def message_type(self) -> int:
        return MessageType.REGISTER.value

    def response_from_json(self, json: dict):
        return RegisterResponseMessage.from_json(json)

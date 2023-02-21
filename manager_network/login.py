from manager_network.messagedata import MessageData, RPCMessage, MessageType
from enum import Enum


class LoginResponseCode(Enum):
    SUCCESS = 0
    INVALID_PASSWORD = 1
    NO_ACCOUNT = 2


class LoginResponseMessage(MessageData):
    def __init__(self, code: LoginResponseCode):
        self.code = code

    def from_json(json: dict):
        return LoginResponseMessage(json["code"])

    def to_json(self) -> dict:
        json = {
            "code": self.code.value
        }
        return json

    def message_type(self) -> int:
        return MessageType.LOGIN_RESPONSE.value


class LoginMessage(RPCMessage):
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def from_json(json: dict):
        return LoginMessage(json["username"], json["password"])

    def to_json(self) -> dict:
        json = {
            "username": self.username,
            "password": self.password
        }
        return json

    def message_type(self) -> int:
        return MessageType.LOGIN.value

    def response_from_json(self, json: dict):
        return LoginResponseMessage.from_json(json)

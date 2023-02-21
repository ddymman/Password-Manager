from typing import Protocol
from abc import abstractmethod
from enum import Enum


class MessageType(Enum):
    GENERIC = 0
    REGISTER = 1
    REGISTER_RESPONSE = 2
    LOGIN = 3
    LOGIN_RESPONSE = 4
    GET_PASSWORDS = 5
    GET_PASSWORDS_RESPONSE = 6
    ADD_PASSWORD = 7
    ADD_PASSWORD_RESPONSE = 8
    DELETE_PASSWORD = 9
    DELETE_ALL_PASSWORDS = 10


class MessageData(Protocol):
    @abstractmethod
    def message_type(self) -> int: int

    @abstractmethod
    def from_json(json: dict): MessageData

    @abstractmethod
    def to_json(self) -> dict: dict


class RPCMessage(MessageData):
    @abstractmethod
    def response_from_json(self, json: dict): None


class NetworkMessage(MessageData):
    message_id: int
    type: int
    data: str

    def __init__(self, message_id: int, type: int, data: str):
        self.message_id = message_id
        self.type = type
        self.data = data

    def to_json(self) -> dict:
        json = {
            "messageid": self.message_id,
            "messagetype": self.type,
            "data": self.data
        }
        return json

    def message_type(self) -> int:
        return self.type

    def from_json(json: dict):
        return NetworkMessage(json["messageid"], json["messagetype"], json["data"])

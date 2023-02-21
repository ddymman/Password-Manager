from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import hashlib


def fernet(password: bytes, salt: bytes) -> Fernet:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    key = kdf.derive(password)
    return Fernet(base64.encodebytes(key))


def encrypt(data: str, password: str) -> str:
    salt = os.urandom(32)
    f = fernet(password.encode(), salt)
    return f.encrypt(data.encode()).hex() + ":" + salt.hex()


def decrypt(data: str, password: str) -> str:
    split_data = data.split(":")
    encrypted = bytes.fromhex(split_data[0])
    salt = bytes.fromhex(split_data[1])

    f = fernet(password.encode(), salt)
    decrypted = f.decrypt(encrypted)
    decoded = decrypted.decode()
    return decoded


def hash_pass(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

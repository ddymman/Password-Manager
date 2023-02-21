class Account:
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def from_json(json: dict):
        return Account(json["username"], json["password"])

    def to_json(self) -> dict:
        j = {
            "username": self.username,
            "password": self.password
        }
        return j

class AppData:
    account: Account

    def __init__(self):
        self.account = None

    def from_json(json: dict):
        data = AppData()
        data.account = Account.from_json(json["account"])
        return data

    def to_json(self) -> dict:
        j = {
            "account": self.account.to_json()
        }
        return j

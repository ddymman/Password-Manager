from manager_client.data.appdata import AppData
import os
import json


def load() -> AppData:
    try:
        f = open("config.json")
        content = f.read()
        f.close()
        return AppData.from_json(json.loads(content))
    except Exception:
        return None


def save(data: AppData):
    try:
        f = open("config.json", "w")
        f.write(json.dumps(data.to_json()))
        f.close()
    except Exception:
        pass


def delete():
    try:
        os.remove("config.json")
    except Exception:
        pass

